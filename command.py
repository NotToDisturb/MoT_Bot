import csv
import os
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
        pass


cmd_to_func = {"csv": Command.generate_csv,
               "poke": Command.poke}
