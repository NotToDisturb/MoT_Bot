import csv
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

import file_utils
import utils
from reaction_handlers.reaction_handler import DeleteHandler
from reaction_handlers.pokes_handler import PokesHandler


load_dotenv()
CSV_POKES = os.getenv("CSV_POKES")


class PokesCog(commands.Cog):
    @commands.command(name="pokes")
    async def pokes_command(self, ctx, *args):
        if len(args) > 0:  # There are arguments
            if args[0] == "skip":  # The first argument is to be skipped
                page = 0
            elif not args[0].isnumeric():  # The first argument is not a number
                page = 0
                await do_unexpected_page(ctx, args[0], 1)
            else:
                page = int(args[0]) - 1
        else:
            page = 0

        if len(args) > 1:  # There is a second argument
            if not args[1].isnumeric():  # The second argument is not a number
                per_page = 10
                await do_unexpected_per_page(ctx, args[1], 10)
            else:
                per_page = int(args[1])
        else:
            per_page = 10

        contents = get_page(page, per_page)
        # PAGE CONTAINS NO POKÉMON
        # Show error message and exit
        if len(contents) == 0:
            await do_page_too_high(ctx, page)
            return

        # EVERYTHING CORRECT
        # Create embedded message and add corresponding reactions
        embed_message = do_embed(page, per_page, contents)
        message = await ctx.send(embed=embed_message)
        await add_reactions(message)
        utils.get_tracker().track_message(message.id, {
            "author": ctx.author.id,
            "page": page,
            "per_page": per_page,
            "reaction_handler": PokesHandler(do_embed, get_page)
        })


async def do_unexpected_page(ctx, incorrect, interpreted):
    embed_message = discord.Embed(title="I didn't quite catch that",
                                  description="You asked about page `" + str(incorrect) + "` " +
                                              " but that doesn't work, so I'll go with " + str(interpreted) + ".",
                                  color=0x52307c)
    bot_message = await ctx.send(embed=embed_message)
    await bot_message.delete(delay=5)


async def do_unexpected_per_page(ctx, incorrect, interpreted):
    embed_message = discord.Embed(title="I didn't quite catch that",
                                  description="You asked about `" + str(incorrect) + "` Pokémon per page " +
                                              "but that doesn't work, so I'll go with " + str(interpreted) + ".",
                                  color=0x52307c)
    bot_message = await ctx.send(embed=embed_message)
    await bot_message.delete(delay=5)


async def do_page_too_high(ctx, page):
    message = await utils.do_simple_embed(
        context=ctx,
        title="Page " + str(page + 1) + " you say?",
        description="I'm afraid the Avlarian Pokédex is not that long."
    )
    utils.get_tracker().track_message(message.id, {
        "author": ctx.author.id,
        "reaction_handler": DeleteHandler()
    })


def do_embed(page, per_page, contents):
    numbers, names = build_page(contents)
    embed_message = discord.Embed(title="Page " + str(page + 1) + "? Yes, here you go",
                                  description="",
                                  color=0x52307c)
    embed_message.add_field(name="Num.", value=numbers)
    embed_message.add_field(name="Pokémon", value=names)
    embed_message.set_footer(text="Page " + str(page + 1) + " - Showing " + str(per_page) + " Pokémon per page")
    return embed_message


def get_page(page, per_page):
    page_contents = []
    with open(file_utils.do_resources_path(CSV_POKES), "rt") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for index, line in enumerate(reader):
            if index >= (page + 1) * per_page:
                break
            if index >= page * per_page:
                page_contents.append(line)
        return page_contents


def build_page(contents):
    numbers = ""
    names = ""
    for line in contents:
        numbers += "Nº " + line["Num"] + "\n"
        names += line["Name"] + "\n"
    return numbers, names


async def add_reactions(message):
    await message.add_reaction("◀️")
    await message.add_reaction("▶️")
    await message.add_reaction("🗑️")


def setup(discord_client):
    discord_client.add_cog(PokesCog(discord_client))
