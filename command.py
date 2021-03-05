import os

from commands.generate_csv import generate_csv
from commands.poke import poke
from commands.none import none

from dotenv import load_dotenv

load_dotenv()
DISCORD_PREFIX = os.getenv("DISCORD_PREFIX")


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
        func = cmd_to_func.get(self.command, None)
        await (func(self.discord_client, self.message, self.command, self.args) if func is not None
               else none(self.discord_client, self.message, self.command, self.args))


cmd_to_func = {"csv": generate_csv,
               "poke": poke}
