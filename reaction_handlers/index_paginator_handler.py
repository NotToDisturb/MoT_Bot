import os

from reaction_handlers.general_handlers import SideArrowsHandler

CSV_POKES = os.getenv("CSV_POKES")
CSV_SOURCES = os.getenv("CSV_SOURCES")


class IndexPaginatorHandler(SideArrowsHandler):
    def __init__(self, build_embed):
        self.build_embed = build_embed

    async def handle_directional_arrow(self, reaction, user, message_data, offset):
        page = message_data["page"] + offset
        per_page = message_data["per_page"]
        pages_total = message_data["pages"]
        if page == pages_total:
            page = 0
        elif page == -1:
            page = pages_total - 1
        message_data["page"] = page
        embed_message = self.build_embed(page, per_page)
        await reaction.message.edit(embed=embed_message)
        await self.update_reactions(reaction.message, page, 0, pages_total)
