import os

import discord
from dotenv import load_dotenv
import command as cmd_utils
from command import Command

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_TESTER = os.getenv("DISCORD_TESTER")

discord_client = discord.Client()


@discord_client.event
async def on_ready():
    print(f"{discord_client.user.name} has connected to Discord!")


@discord_client.event
async def on_message(message):
    if cmd_utils.is_prof_command(message):
        command = Command(discord_client, message)
        await command.execute()

discord_client.run(DISCORD_TOKEN)
