import csv
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

import file_utils
import utils
from reaction_handlers.general_handlers import DeleteHandler
from paginators.index_paginator import IndexPaginator

load_dotenv()
CSV_SOURCES = os.getenv("CSV_SOURCES")


class SourcesCog(commands.Cog):
    @commands.command(name="sources")
    async def sources_command(self, ctx, *args):
        await IndexSources(ctx, args, 10).start()


class IndexSources(IndexPaginator):
    async def do_unexpected_page(self, incorrect, interpreted):
        embed_message = discord.Embed(title="I didn't quite catch that",
                                      description=f"You asked about page `{incorrect}` " +
                                                  f" but that doesn't work, so I'll go with {interpreted}.",
                                      color=0x52307c)
        bot_message = await self.ctx.send(embed=embed_message)
        await bot_message.delete(delay=5)

    async def do_unexpected_per_page(self, incorrect, interpreted):
        embed_message = discord.Embed(title="I didn't quite catch that",
                                      description=f"You asked about `{incorrect}` sources per page " +
                                                  f"but that doesn't work, so I'll go with {interpreted}.",
                                      color=0x52307c)
        bot_message = await self.ctx.send(embed=embed_message)
        await bot_message.delete(delay=5)

    async def do_page_too_high(self, page):
        message = await utils.do_simple_embed(
            context=self.ctx,
            title=f"Page {page + 1} you say?",
            description="There's not that many sources!"
        )
        utils.get_tracker().track_message(message.id, {
            "author": self.ctx.author.id,
            "reaction_handler": DeleteHandler()
        })

    def do_embed(self, page, per_page, contents):
        numbers, names, links = self.build_page(contents, page * per_page)
        embed_message = discord.Embed(title=f"Page {page + 1}? Yes, here you go",
                                      description="",
                                      color=0x52307c)
        embed_message.add_field(name="Num.", value=numbers)
        embed_message.add_field(name="Source", value=names)
        embed_message.add_field(name="Link", value=links)
        embed_message.set_footer(text=f"Page {page + 1} - Showing {per_page} sources per page")
        return embed_message

    def get_pages(self, page, per_page):
        pages_total = file_utils.get_num_of_rows(CSV_SOURCES) // per_page
        return pages_total + 1 if file_utils.get_num_of_rows(CSV_SOURCES) % per_page > 0 else 0

    def get_page_contents(self, page, per_page):
        page_contents = []
        with open(file_utils.do_resources_path(CSV_SOURCES), "rt") as csv_file:
            reader = csv.DictReader(csv_file, delimiter=',')
            for index, line in enumerate(reader):
                if index >= (page + 1) * per_page:
                    break
                if index >= page * per_page:
                    page_contents.append(line)
            return page_contents

    @staticmethod
    def build_page(contents, offset):
        numbers = ""
        names = ""
        links = ""
        for index, line in enumerate(contents):
            numbers += f'Nº{str(offset + index + 1)}\n'
            names += f'{line["Name"]}\n'
            links += ", ".join([f'[Go]({link})' for link in line["Link"].split("|")]) + "\n"
        return numbers, names, links


def setup(discord_client):
    discord_client.add_cog(SourcesCog(discord_client))
