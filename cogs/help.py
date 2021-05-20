import json
import os
import discord

from dotenv import load_dotenv
from discord.ext import commands

from utils import get_config, get_tracker
from reaction_handlers.reaction_handler import DeleteHandler

load_dotenv()
DISCORD_PREFIX = os.getenv("DISCORD_PREFIX")


def load_messages():
    with open("configs/help_messages.json", "rt", encoding="utf-8") as messages:
        return json.load(messages)


class HelpCog(commands.Cog):
    messages = get_config("help_messages")

    @commands.command(name="help")
    async def help_command(self, ctx, *option):
        if len(option) == 0:
            message_key = ""
        elif option[0] in self.messages["messages"].keys():
            message_key = option[0]
        else:
            message_key = "fallback"
        embed_message = self.build_help_embed(message_key)
        message = await ctx.send(embed=embed_message)
        await message.add_reaction("🗑️")
        get_tracker().track_message(message.id, {
            "author": ctx.author.id,
            "reaction_handler": DeleteHandler()
        })

    def build_help_embed(self, message_key):
        message_contents = self.messages["messages"][message_key]
        description = message_contents["description"].replace("{prefix}", DISCORD_PREFIX)\
            .replace("{options}", self.messages["global"]["options"])

        embed_message = discord.Embed(title=message_contents["title"],
                                      description=description,
                                      color=int(self.messages["global"]["color"], 16))
        for field in message_contents.get("fields", []):
            embed_message.add_field(name=field["name"],
                                    value=field["value"],
                                    inline=field["inline"])
        return embed_message


def setup(discord_client):
    discord_client.add_cog(HelpCog(discord_client))
