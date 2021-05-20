import os

from dotenv import load_dotenv
from discord.ext import commands

import utils
from reaction_handlers.reaction_handler import DeleteHandler

load_dotenv()
DISCORD_PREFIX = os.getenv("DISCORD_PREFIX")


class InfoCog(commands.Cog):
    @commands.command(name="info")
    async def info_command(self, ctx):
        message = await utils.do_simple_embed(
            context=ctx,
            title="Hello, I am Professor Till!",
            description="I've been exploring the Avlar Region for quite some time now, "
                        "time that has allowed me to gain knowledge on various fields!\n\n"
                        "Like many other partners in my profession my specialty is Pokémon, "
                        "but don't be afraid to ask about something else.\n\n"
                        "You can learn more about this region and its Pokémon by using"
                        f"`{DISCORD_PREFIX}help`.",
        )
        utils.get_tracker().track_message(message.id, {
            "author": ctx.author.id,
            "reaction_handler": DeleteHandler()
        })


def setup(discord_client):
    discord_client.add_cog(InfoCog(discord_client))
