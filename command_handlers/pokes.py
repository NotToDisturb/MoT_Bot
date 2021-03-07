import csv
import os

import discord
from dotenv import load_dotenv

import file_utils

load_dotenv()
CSV_POKES = os.getenv("CSV_POKES")


async def pokes_command(discord_client, message, command, args):
    page_raw = args.split(" ")
    if len(page_raw) > 0:
        if page_raw[0] == "skip":
            page = 0
        elif not page_raw[0].isnumeric():
            page = 0
            await pokes_do_unexpected(message, page_raw[0], 1)
        else:
            page = int(page_raw[0]) - 1
    else:
        page = 0

    if len(page_raw) > 1:
        if not page_raw[1].isnumeric():
            per_page = 10
            await pokes_do_unexpected(message, page_raw[1], 10)
        else:
            per_page = int(page_raw[1])
    else:
        per_page = 10

    contents = pokes_fetch_page(page, per_page)

    if len(contents) > 0:
        embed_message = pokes_do_embed(page, per_page, contents)

        bot_message = await message.channel.send(embed=embed_message)

        await pokes_do_reactions(bot_message, page, per_page)
    else:
        embed_message = discord.Embed(title="Page " + str(page + 1) + " you say?",
                                      description="I'm afraid that's not in the Avlarian Pokédex.",
                                      color=0x52307c)

        bot_message = await message.channel.send(embed=embed_message)

        await bot_message.add_reaction("🗑️")


async def pokes_do_unexpected(message, incorrect, interpreted):
    embed_message = discord.Embed(title="I didn't quite catch that",
                                  description="You asked about " + str(incorrect) +
                                              " but that doesn't work, so I'll go with " + str(interpreted) + ".",
                                  color=0x52307c)

    bot_message = await message.channel.send(embed=embed_message)

    await bot_message.delete(delay=5)


def pokes_do_embed(page, per_page, contents):
    page_contents = pokes_do_page(contents)

    embed_message = discord.Embed(title="Page " + str(page + 1) + "? Yes, here you go",
                                  description=page_contents,
                                  color=0x52307c)

    embed_message.set_footer(text="Page " + str(page + 1) + " - Showing " + str(per_page) + " Pokémon per page")

    return embed_message


def pokes_fetch_page(page, per_page):
    page_contents = []
    with open(file_utils.do_resources_path(CSV_POKES), "rt") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for index, line in enumerate(reader):
            if index >= (page + 1) * per_page:
                break
            elif index >= page * per_page:
                page_contents.append(line)
        return page_contents


def pokes_do_page(contents):
    page_contents = ""
    for line in contents:
        page_contents += "Nº" + line["Num"] + " - " + line["Name"] + "\n"
    return page_contents


async def pokes_do_reactions(message, page, per_page):
    if page > 0:
        await message.add_reaction("◀️")
    if (page + 1) * per_page < file_utils.get_num_of_rows(CSV_POKES):
        await message.add_reaction("▶️")
    await message.add_reaction("🗑️")


