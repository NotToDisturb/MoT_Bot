import csv
import os

import discord

import sheets_utils

from dotenv import load_dotenv

load_dotenv()
SHEET_ID = os.getenv("SHEET_ID")
DISCORD_PREFIX = os.getenv("DISCORD_PREFIX")
DISCORD_TESTER = os.getenv("DISCORD_TESTER")
CSV_POKES = os.getenv("CSV_POKES")
CSV_SOURCES = os.getenv("CSV_SOURCES")


def is_prof_command(message):
    return message.content.startswith(DISCORD_PREFIX)


class Command:
    def __init__(self, discord_client, message):
        self.discord_client = discord_client
        self.message = message
        split_content = message.content[len(DISCORD_PREFIX):].split(" ", 1)
        self.command = split_content[0]
        self.args = split_content[1] if len(split_content) > 1 else ""

    async def execute(self):
        await cmd_to_func.get(self.command, self.none)(self)

    async def none(self):
        pass

    async def generate_csv(self):
        if str(self.message.author) == str(self.discord_client.user) or str(self.message.author) == str(DISCORD_TESTER):
            spreadsheet = sheets_utils.open_spreadsheet(SHEET_ID)
            sheets_utils.generate_spreadsheet_csv(spreadsheet)
            await self.message.channel.send("CSV files have been rebuilt")
        else:
            await self.message.channel.send("Not enough permission to rebuild CSV files")

    async def poke(self):
        index = sheets_utils.get_index_in_column(CSV_POKES, "Name", self.args)
        if index > -1:
            pokedex_num = sheets_utils.get_element_in_column(CSV_POKES, "Num", index)
            image = sheets_utils.get_element_in_column(CSV_POKES, "Image", index)
            notes = sheets_utils.get_element_in_column(CSV_POKES, "Notes", index)
            sources = sheets_utils.get_element_in_column(CSV_POKES, "Sources", index).split("|")

            embed_message = discord.Embed(title="Nº" + str(pokedex_num) + " - " + self.args, color=0x52307c)
            embed_message.set_thumbnail(url=image)

            if len(sources) > 0:
                sources_value = ""
                for source_index in range(0, len(sources)):
                    source_name = sheets_utils.get_element_in_column(CSV_SOURCES, "Name", int(sources[source_index]))
                    source_value = sheets_utils.get_element_in_column(CSV_SOURCES, "Link", int(sources[source_index]))
                    sources_value += "\n[" + source_name +  "](" + source_value + ")"
                embed_message.add_field(name="Sources", value=sources_value, inline=False)
            if len(notes) > 0:
                embed_message.add_field(name="Dev notes", value=notes, inline=False)
            await self.message.channel.send(embed=embed_message)
        else:
            await self.message.channel.send(self.args + " is not in the Avlarian Pokédex")


cmd_to_func = {"csv": Command.generate_csv,
               "poke": Command.poke}
