import os

import discord
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_TESTER = os.getenv("DISCORD_TESTER")

discord_client = discord.Client()


@discord_client.event
async def on_ready():
    print(f"{discord_client.user.name} has connected to Discord!")


@discord_client.event
async def on_message(message):
    pass

discord_client.run(DISCORD_TOKEN)
