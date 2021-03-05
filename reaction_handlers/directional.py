import os

from dotenv import load_dotenv

import file_utils
from command_handlers import poke

load_dotenv()
CSV_POKES = os.getenv("CSV_POKES")
CSV_SOURCES = os.getenv("CSV_SOURCES")


async def handle_directional_poke(reaction, user, direction):
    num = reaction.message.embeds[0].title.replace("Nº", "").split(" - ")[0]
    index = file_utils.get_index_in_column(CSV_POKES, "Num", num) + get_direction_offset(direction)
    line = file_utils.get_line_at_row(CSV_POKES, index)

    embed_message = poke.poke_do_embed(line)
    await reaction.message.edit(embed=embed_message)

    await reaction.message.clear_reactions()
    await poke.poke_do_reactions(reaction.message, index)


def get_message_type(message):
    title = message.embeds[0].title
    if title.startswith("Nº"):
        return 0


def get_direction_offset(direction):
    if direction == "back":
        return -1
    if direction == "forward":
        return 1


type_to_func = [handle_directional_poke]


async def back_reaction(reaction, user):
    reaction_type = get_message_type(reaction.message)
    await type_to_func[reaction_type](reaction, user, "back")


async def forward_reaction(reaction, user):
    reaction_type = get_message_type(reaction.message)
    await type_to_func[reaction_type](reaction, user, "forward")
