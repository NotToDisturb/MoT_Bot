import os

from command_handlers.info import info_command
from command_handlers.help import help_command
from command_handlers.generate_csv import generate_csv_command
from command_handlers.poke import poke_command
from command_handlers.stories import stories_command
from command_handlers.story import story_command
from command_handlers.none import none_command

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
               else none_command(self.discord_client, self.message, self.command, self.args))


cmd_to_func = {"help": help_command,
               "info": info_command,
               "csv": generate_csv_command,
               "poke": poke_command,
               "stories": stories_command,
               "story": story_command}
