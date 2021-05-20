import csv
import os
import discord

from dotenv import load_dotenv
from discord.ext import commands

import file_utils
import utils
from reaction_handlers.reaction_handler import DeleteHandler
from reaction_handlers.poke_handler import PokeHandler


load_dotenv()
CSV_POKES = os.getenv("CSV_POKES")
CSV_SOURCES = os.getenv("CSV_SOURCES")


class PokeCog(commands.Cog):
    @commands.command(name="poke")
    async def poke_command(self, ctx, *, poke):
        if not poke.isnumeric():
            line, index = file_utils.find_item_in_columns_and_get_row(CSV_POKES, "Name", poke)
        else:
            line, index = file_utils.find_item_in_columns_and_get_row(CSV_POKES, "Num", poke)

        # MON NAME OR NUMBER NOT FOUND IN CSV
        # Show error message and return
        if line == - 1:
            await do_not_in_dex(ctx, poke)
            return

        # EVERYTHING CORRECT
        # Create embedded message and add corresponding reactions
        embed_message = do_embed(line)
        message = await ctx.send(embed=embed_message)
        await add_reactions(message)
        utils.get_tracker().track_message(message.id, {
            "author": ctx.author.id,
            "dex_num": line["Num"],
            "reaction_handler": PokeHandler(do_embed)
        })


async def do_not_in_dex(ctx, poke):
    message = await utils.do_simple_embed(
        context=ctx,
        title="I have some bad news...",
        description=f"{poke} is not in the Avlarian Pokédex."
    )
    utils.get_tracker().track_message(message.id, {
        "author": ctx.author.id,
        "reaction_handler": DeleteHandler()
    })


def do_embed(line):
    name = line["Name"]
    embed_message = discord.Embed(title="Nº" + line["Num"] + " - " + name,
                                  description="Let's see, what can I tell you about " + name + "...",
                                  color=0x52307c)
    embed_message.set_thumbnail(url=line["Image"])

    sources_title, sources_value = get_sources(line)
    embed_message.add_field(name=sources_title, value=sources_value, inline=False)

    notes = line["Notes"]
    if len(notes) > 0:
        embed_message.add_field(name="Oh, and some extra notes", value=notes, inline=False)

    return embed_message


def get_source_lines(sources):
    source_lines = []
    with open(file_utils.do_resources_path(CSV_SOURCES), "rt") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for csv_index, line in enumerate(reader):
            if str(csv_index) in sources:
                source_lines.append(line)
    return source_lines


def get_sources(line):
    sources_raw = line["Sources"]
    if len(sources_raw) > 0:
        return build_sources_spotted(sources_raw)
    else:
        return build_sources_evolutions(line)


def build_sources_spotted(sources_raw):
    sources = sources_raw.split("|")
    source_lines = get_source_lines(sources)
    sources_value = ""
    for source_line in source_lines:
        source_name = source_line["Name"]
        source_value = source_line["Link"]
        sources_value += "\n[" + source_name + "](" + source_value + ")"
    return "It's been spotted!", sources_value


def build_sources_evolutions(line):
    evolutions = line["Evolves"].split("|")
    has_from, has_to = False, False
    from_text = "__Spotted pre-evolutions:__"
    to_text = "__Spotted evolutions:__"
    for evo_raw in evolutions:
        evolution = evo_raw.split(":")
        if evolution[0] == "from":
            from_text += "\n" + evolution[1]
            has_from = True
        else:
            to_text += "\n" + evolution[1]
            has_to = True
    return "We've seen part of its line!", (from_text + "\n\n" if has_from else "") + (to_text if has_to else "")


async def add_reactions(message):
    await message.add_reaction("◀️")
    await message.add_reaction("▶️")
    await message.add_reaction("🗑️")


def setup(discord_client):
    discord_client.add_cog(PokeCog(discord_client))
