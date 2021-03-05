import os

import discord

from dotenv import load_dotenv

load_dotenv()
DISCORD_PREFIX = os.getenv("DISCORD_PREFIX")


async def info_command(discord_client, message, command, args):
    embed_message = discord.Embed(title="Hello, I am the Professor!",
                                  description="I keep track of all things related to Mirage of Tales, mostly the "
                                              "Pokémon you will find in the Avlar Region. \n\n "
                                              "Learn more about what I do by using `" + DISCORD_PREFIX + "help`",
                                  color=0x52307c)
    embed_message.set_footer(text="Built by Disturbo",
                             icon_url="https://avatars.githubusercontent.com/u/16744563?s=460&u"
                                      "=e570ce6dbdb0c6ff2f3b5e4e116090b7b4b1a9e6")
    await message.channel.send(embed=embed_message)
