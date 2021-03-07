import os

from dotenv import load_dotenv

import file_utils
from command_handlers import poke, pokes, story

load_dotenv()

CSV_POKES = os.getenv("CSV_POKES")
CSV_SOURCES = os.getenv("CSV_SOURCES")

CSV_STORY_GROUPS = os.getenv("CSV_STORY_GROUPS")
CSV_STORIES = os.getenv("CSV_STORIES")


async def handle_directional_poke(reaction, user, direction):
    num = reaction.message.embeds[0].title.replace("Nº", "").split(" - ")[0]
    index = file_utils.get_index_in_column(CSV_POKES, "Num", num) + get_direction_offset(direction)
    line = file_utils.get_line_at_row(CSV_POKES, index)

    embed_message = poke.poke_do_embed(line)
    await reaction.message.edit(embed=embed_message)

    await reaction.message.clear_reactions()
    await poke.poke_do_reactions(reaction.message, index)


async def handle_directional_pokes(reaction, user, direction):
    footer = reaction.message.embeds[0].footer.text
    page_raw = footer.replace("Page ", "").replace(" Pokémon per page", "").split(" - Showing")
    page = int(page_raw[0]) - 1 + get_direction_offset(direction)
    per_page = int(page_raw[1])
    contents = pokes.pokes_fetch_page(page, per_page)

    embed_message = pokes.pokes_do_embed(page, per_page, contents)
    await reaction.message.edit(embed=embed_message)

    await reaction.message.clear_reactions()
    await pokes.pokes_do_reactions(reaction.message, page, per_page)


async def handle_directional_story(reaction, user, direction):
    story_raw = reaction.message.embeds[0].fields[0].name.split(" - Part")
    line, index = file_utils.find_item_in_columns_and_get_row(CSV_STORIES, "Name", story_raw[0])
    part = int(story_raw[1]) - 1 + get_direction_offset(direction)
    parts = int(line["Parts"])

    embed_message = story.story_do_embed(line, part)
    await reaction.message.edit(embed=embed_message)

    await reaction.message.clear_reactions()
    await story.story_do_reactions(reaction.message, parts, part)


def get_message_type(message):
    title = message.embeds[0].title
    if title.startswith("Nº"):
        return 0
    elif title.startswith("Page "):
        return 1
    elif title == "Story time!":
        return 2


def get_direction_offset(direction):
    if direction == "back":
        return -1
    if direction == "forward":
        return 1


type_to_func = [handle_directional_poke,
                handle_directional_pokes,
                handle_directional_story]


async def back_reaction(reaction, user):
    reaction_type = get_message_type(reaction.message)
    await type_to_func[reaction_type](reaction, user, "back")


async def forward_reaction(reaction, user):
    reaction_type = get_message_type(reaction.message)
    await type_to_func[reaction_type](reaction, user, "forward")
