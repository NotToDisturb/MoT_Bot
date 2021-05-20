import os

import file_utils
from reaction_handlers.reaction_handler import SideArrowsHandler

CSV_POKES = os.getenv("CSV_POKES")
CSV_SOURCES = os.getenv("CSV_SOURCES")


class PokesHandler(SideArrowsHandler):
    def __init__(self, do_embed, get_page):
        self.do_embed = do_embed
        self.get_page = get_page

    async def handle_directional_arrow(self, reaction, user, message_data, offset):
        page = message_data["page"] + offset
        per_page = message_data["per_page"]
        pages_total = file_utils.get_num_of_rows(CSV_POKES) // per_page
        pages_total += 1 if file_utils.get_num_of_rows(CSV_POKES) % per_page > 0 else 0
        if page == pages_total:
            page = 0
        elif page == -1:
            page = pages_total - 1
        contents = self.get_page(page, per_page)
        message_data["page"] = page
        embed_message = self.do_embed(page, per_page, contents)
        await reaction.message.edit(embed=embed_message)
        await self.update_reactions(reaction.message, page, 0, pages_total)
