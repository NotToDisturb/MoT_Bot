import os

import discord
from dotenv import load_dotenv

import sheets_utils

load_dotenv()
CSV_POKES = os.getenv("CSV_POKES")
CSV_SOURCES = os.getenv("CSV_SOURCES")


async def poke(discord_client, message, command, args):
    line, index = sheets_utils.find_item_in_columns_and_get_row(CSV_POKES, "Name", args)
    if index > -1:
        title = "Nº" + line["Num"] + " - " + line["Name"]

        embed_message = discord.Embed(title=title, color=0x52307c)
        embed_message.set_thumbnail(url=line["Image"])

        sources_title, sources_value = poke_do_sources(line)
        embed_message.add_field(name=sources_title, value=sources_value, inline=False)

        notes = line["Notes"]
        if len(notes) > 0:
            embed_message.add_field(name="Dev notes", value=notes, inline=False)

        await message.channel.send(embed=embed_message)
    else:
        await message.channel.send(args + " is not in the Avlarian Pokédex")


def poke_do_sources(line):
    sources_raw = line["Sources"]
    sources_value = ""
    if len(sources_raw) > 0:
        sources = sources_raw.split("|")
        for source_index in range(0, len(sources)):
            source_name = sheets_utils.get_element_in_column(CSV_SOURCES, "Name", int(sources[source_index]))
            source_value = sheets_utils.get_element_in_column(CSV_SOURCES, "Link", int(sources[source_index]))
            sources_value += "\n[" + source_name + "](" + source_value + ")"
        return "Sources", sources_value
    else:
        evolutions = line["Evolves"].split("|")
        has_from, has_to = False, False
        from_text = "__Pre-evolutions with source:__"
        to_text = "__Evolutions with source:__"
        for evo_raw in evolutions:
            evolution = evo_raw.split(":")
            if evolution[0] == "from":
                from_text += "\n" + evolution[1]
                has_from = True
            else:
                to_text += "\n" + evolution[1]
                has_to = True
        return "Evolution sources", (from_text + "\n\n" if has_from else "") + (to_text if has_to else "")