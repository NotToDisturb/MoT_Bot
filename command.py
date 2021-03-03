import os
import g_sheets

from dotenv import load_dotenv

load_dotenv()
SHEET_ID = os.getenv("SHEET_ID")
DISCORD_PREFIX = os.getenv("DISCORD_PREFIX")
DISCORD_TESTER = os.getenv("DISCORD_TESTER")


def is_prof_command(message):
    return message.content.startswith(DISCORD_PREFIX)


class Command:
    def __init__(self, discord_client, message):
        self.discord_client = discord_client
        self.message = message
        split_content = message.content[len(DISCORD_PREFIX):].split(" ", 1)
        self.command = split_content[0]
        self.args = split_content[0] if len(split_content) > 0 else ""

    async def execute(self):
        await cmd_to_func.get(self.command, self.none)(self)

    async def none(self):
        pass

    async def generate_csv(self):
        if str(self.message.author) == str(self.discord_client.user) or str(self.message.author) == str(DISCORD_TESTER):
            spreadsheet = g_sheets.open_spreadsheet(SHEET_ID)
            g_sheets.generate_spreadsheet_csv(spreadsheet)
            await self.message.channel.send("CSV files have been rebuilt")
        else:
            await self.message.channel.send("Not enough permission to rebuild CSV files")

    async def mon(self):
        pass


cmd_to_func = {"csv": Command.generate_csv,
               "mon": Command.mon}
