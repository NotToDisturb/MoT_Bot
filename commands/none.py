import os

import discord

from dotenv import load_dotenv

load_dotenv()
DISCORD_PREFIX = os.getenv("DISCORD_PREFIX")


async def none(discord_client, message, command, args):
    embed_message = discord.Embed(title="Usage",
                                  description="The command " + DISCORD_PREFIX + command + " doesn't exist.",
                                  color=0x52307c)
    await message.channel.send(embed=embed_message)
