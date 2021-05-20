import csv
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

import file_utils
import utils
from reaction_handlers.reaction_handler import DeleteHandler
from paginator import IndexPaginator

load_dotenv()
CSV_SOURCES = os.getenv("CSV_SOURCES")


class SourcesCog(commands.Cog):
    @commands.command(name="sources")
    async def sources_command(self, ctx, *args):
        await IndexSources(ctx, args).start()


class IndexSources(IndexPaginator):
    async def do_unexpected_page(self, ctx, incorrect, interpreted):
        embed_message = discord.Embed(title="I didn't quite catch that",
                                      description="You asked about page `" + str(incorrect) + "` " +
                                                  " but that doesn't work, so I'll go with " + str(interpreted) + ".",
                                      color=0x52307c)
        bot_message = await ctx.send(embed=embed_message)
        await bot_message.delete(delay=5)

    async def do_unexpected_per_page(self, ctx, incorrect, interpreted):
        embed_message = discord.Embed(title="I didn't quite catch that",
                                      description="You asked about `" + str(incorrect) + "` sources per page " +
                                                  "but that doesn't work, so I'll go with " + str(interpreted) + ".",
                                      color=0x52307c)
        bot_message = await ctx.send(embed=embed_message)
        await bot_message.delete(delay=5)

    async def do_page_too_high(self, ctx, page):
        message = await utils.do_simple_embed(
            context=ctx,
            title="Page " + str(page + 1) + " you say?",
            description="There's not that many sources!"
        )
        utils.get_tracker().track_message(message.id, {
            "author": ctx.author.id,
            "reaction_handler": DeleteHandler()
        })

    def do_embed(self, page, per_page, contents):
        numbers, names, links = self.build_page(contents, page * per_page)
        embed_message = discord.Embed(title="Page " + str(page + 1) + "? Yes, here you go",
                                      description="",
                                      color=0x52307c)
        embed_message.add_field(name="Num.", value=numbers)
        embed_message.add_field(name="Source", value=names)
        embed_message.add_field(name="Link", value=links)
        embed_message.set_footer(text="Page " + str(page + 1) + " - Showing " + str(per_page) + " sources per page")
        return embed_message

    def get_pages(self, per_page):
        pages_total = file_utils.get_num_of_rows(CSV_SOURCES) // per_page
        return pages_total + 1 if file_utils.get_num_of_rows(CSV_SOURCES) % per_page > 0 else 0

    def get_page(self, page, per_page):
        page_contents = []
        with open(file_utils.do_resources_path(CSV_SOURCES), "rt") as csv_file:
            reader = csv.DictReader(csv_file, delimiter=',')
            for index, line in enumerate(reader):
                if index >= (page + 1) * per_page:
                    break
                if index >= page * per_page:
                    page_contents.append(line)
            return page_contents

    def build_page(self, contents, offset):
        numbers = ""
        names = ""
        links = ""
        for index, line in enumerate(contents):
            numbers += f'Nº{str(offset + index + 1)}\n'
            names += f'{line["Name"]}\n'
            links += ", ".join([f'[Go]({link})' for link in line["Link"].split("|")]) + "\n"
        return numbers, names, links

    async def add_reactions(self, message, page, per_page, pages):
        await message.add_reaction("◀️")
        await message.add_reaction("▶️")
        await message.add_reaction("🗑️")


def setup(discord_client):
    discord_client.add_cog(SourcesCog(discord_client))
