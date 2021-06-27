import csv
import os
import discord

from dotenv import load_dotenv
from discord.ext import commands

import file_utils
import utils

from paginators.paginator import Paginator
from reaction_handlers.general_handlers import DeleteHandler
from reaction_handlers.poke_handler import PokeHandler


load_dotenv()
CSV_POKES = os.getenv("CSV_POKES")
CSV_SOURCES = os.getenv("CSV_SOURCES")


class PokeCog(commands.Cog):
    @commands.command(name="poke")
    async def poke_command(self, ctx, *, poke):
        await PokePaginator(ctx, poke).start()


class PokePaginator(Paginator):
    async def do_page_too_high(self, page):
        message = await utils.do_simple_embed(
            context=self.ctx,
            title="I have some bad news...",
            description=f"{page} is not in the Avlarian Pokédex."
        )
        utils.get_tracker().track_message(message.id, {
            "author": self.ctx.author.id,
            "reaction_handler": DeleteHandler()
        })

    async def get_page(self):
        if not self.args.isnumeric():
            line, index = file_utils.find_item_in_columns_and_get_row(CSV_POKES, "Name", self.args)
        else:
            line, index = file_utils.find_item_in_columns_and_get_row(CSV_POKES, "Num", self.args)
        return line

    async def get_per_page(self):
        return 1

    async def get_pages(self, page, per_page):
        return file_utils.get_num_of_rows(CSV_POKES)

    async def do_page_validity(self, page, pages):
        if page == - 1:
            await self.do_page_too_high(self.ctx, page)
            return False
        return True

    def build_embed(self, page, per_page):
        name = page["Name"]
        embed_message = discord.Embed(title=f'Nº{page["Num"]} - {name}',
                                      description=f"Let's see, what can I tell you about {name}...",
                                      color=0x52307c)
        embed_message.set_thumbnail(url=page["Image"])

        sources_title, sources_value = get_sources(page)
        embed_message.add_field(name=sources_title, value=sources_value, inline=False)

        notes = page["Notes"]
        if len(notes) > 0:
            embed_message.add_field(name="Oh, and some extra notes", value=notes, inline=False)

        return embed_message

    def track_message(self, message, page, per_page, pages):
        utils.get_tracker().track_message(message.id, {
            "author": self.ctx.author.id,
            "dex_num": page["Num"],
            "dex_entries": pages,
            "reaction_handler": PokeHandler(self.build_embed)
        })


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
        sources_value += f'\n[{source_line["Name"]}]({source_line["Link"]})'
    return "It's been spotted!", sources_value


def build_sources_evolutions(line):
    evolutions = line["Evolves"].split("|")
    has_from, has_to = False, False
    from_text = "__Spotted pre-evolutions:__"
    to_text = "__Spotted evolutions:__"
    for evo_raw in evolutions:
        evolution = evo_raw.split(":")
        if evolution[0] == "from":
            from_text += f"\n{evolution[1]}"
            has_from = True
        else:
            to_text += f"\n{evolution[1]}"
            has_to = True
    return "We've seen part of its page!", (f"{from_text}\n\n" if has_from else "") + (to_text if has_to else "")


def get_source_lines(sources):
    with open(file_utils.do_resources_path(CSV_SOURCES), "rt") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        return [line for csv_index, line in enumerate(reader)
                if str(csv_index) in sources]


def setup(discord_client):
    discord_client.add_cog(PokeCog(discord_client))
