import os

import discord

from dotenv import load_dotenv

load_dotenv()
DISCORD_PREFIX = os.getenv("DISCORD_PREFIX")
DISTURBO_ICON = os.getenv("DISTURBO_ICON")


async def help_command(discord_client, message, command, args):
    embed_message = discord.Embed(title="You have a doubt? No prob!",
                                  description="These are all the things I can do:",
                                  color=0x52307c)
    embed_message.add_field(name="Info",
                            value=build_usage_string("info") + "Will tell you bit about myself.",
                            inline=False)
    embed_message.add_field(name="Poke",
                            value=build_usage_string("poke <name>") + "This is the command to execute"
                                                                      "if you want information on a specific Pokémon",
                            inline=False)
    embed_message.set_footer(text="Built by Disturbo",
                             icon_url=DISTURBO_ICON)
    await message.channel.send(embed=embed_message)


def build_usage_string(command):
    return "__Usage:__ `" + DISCORD_PREFIX + command + "`\n"
