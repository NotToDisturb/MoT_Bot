import os

import discord

from dotenv import load_dotenv

load_dotenv()
DISCORD_PREFIX = os.getenv("DISCORD_PREFIX")


async def none_command(discord_client, message, command, args):
    embed_message = discord.Embed(title="I didn't quite catch that",
                                  description="`" + DISCORD_PREFIX + command + "` doesn't exist! "
                                              "Use `" + DISCORD_PREFIX + "help` to check out all the commands.",
                                  color=0x52307c)
    await message.channel.send(embed=embed_message)
