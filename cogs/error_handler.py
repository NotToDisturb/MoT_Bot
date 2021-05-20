import os

import discord
from dotenv import load_dotenv

from discord.ext import commands

from utils import get_config

load_dotenv()
DISCORD_PREFIX = os.getenv("DISCORD_PREFIX")


class ErrorHandlerCog(commands.Cog):
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            try:
                command = ctx.invoked_with
            except AttributeError:
                description = f"Couldn't even understand which command you used!"
            else:
                description = f"The command `{DISCORD_PREFIX}{command}` doesn't exist, " \
                              f"try using `{DISCORD_PREFIX}help` for more information."
        elif isinstance(error, commands.MissingRequiredArgument):
            description = "I know more or less what you want, but I'm missing an argument!\n"
            try:
                command = ctx.invoked_with
            except AttributeError:
                pass
            else:
                usages = [usage.replace("{prefix}", DISCORD_PREFIX) for usage in get_config("usages")[command]]
                if len(usages) == 1:
                    description += f"The correct usage is {usages[0]}"
                else:
                    description += "The correct usages for this command are:\n" + "\n".join(usages)
        elif isinstance(error, commands.UnexpectedQuoteError):
            description = "Can you repeat what you said? Make sure that the quotation marks are correct."
        else:
            description = "I'll have to add this to my pending research."
            print("[WARNING] Unhandled command error")

        embed = discord.Embed(title="I didn't quite catch that",
                              description=description,
                              color=0x52307c)
        message = await ctx.send(embed=embed)
        await message.delete(delay=5)


def setup(discord_client):
    discord_client.add_cog(ErrorHandlerCog(discord_client))