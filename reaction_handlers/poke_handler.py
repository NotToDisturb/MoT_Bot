import os

import file_utils
from reaction_handlers.reaction_handler import SideArrowsHandler

CSV_POKES = os.getenv("CSV_POKES")
CSV_SOURCES = os.getenv("CSV_SOURCES")


class PokeHandler(SideArrowsHandler):
    def __init__(self, do_embed):
        self.do_embed = do_embed

    async def handle_directional_arrow(self, reaction, user, message_data, offset):
        lines = file_utils.get_num_of_rows(CSV_POKES)
        index = file_utils.get_index_in_column(CSV_POKES, "Num", message_data["dex_num"]) + offset
        if index == lines:
            index = 0
        elif index == -1:
            index = lines - 1
        line = file_utils.get_line_at_row(CSV_POKES, index)
        message_data["dex_num"] = line["Num"]
        embed_message = self.do_embed(line)
        await reaction.message.edit(embed=embed_message)
        await self.update_reactions(reaction.message, index, 0, lines)
