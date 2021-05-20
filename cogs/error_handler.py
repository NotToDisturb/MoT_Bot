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
            title = "I didn't quite catch that"
            command = get_command(ctx)
            description = f"The command `{DISCORD_PREFIX}{command}` doesn't exist, " \
                          f"try using `{DISCORD_PREFIX}help` for more information." \
                          if command else \
                          "Couldn't even understand which command you used!"
        elif isinstance(error, commands.MissingRequiredArgument):
            title = "I didn't quite catch that"
            description = "I know more or less what you want, but I'm missing an argument!\n"
            command = get_command(ctx)
            if command:
                usages = [usage.replace("{prefix}", DISCORD_PREFIX) for usage in get_config("usages")[command]]
                description += f"The correct usage is {usages[0]}" \
                               if len(usages) == 1 else \
                               "The correct usages for this command are:\n" + "\n".join(usages)
        elif isinstance(error, commands.UnexpectedQuoteError):
            title = "I didn't quite catch that"
            description = "Can you repeat what you said? Make sure that the quotation marks are correct."
        elif isinstance(error, commands.MissingPermissions):
            title = "Uh oh"
            command = get_command(ctx)
            if command:
                description = f"You don't have permissions to use `{DISCORD_PREFIX}{command}`!"
        else:
            title = "I didn't quite catch that"
            description = "I'll have to add this to my pending research."
            print(f"[WARNING] Unhandled command error:\n{str(error)}")

        embed = discord.Embed(title=title,
                              description=description,
                              color=0x52307c)
        message = await ctx.send(embed=embed)
        await message.delete(delay=10)


def get_command(ctx):
    try:
        command = ctx.invoked_with
    except AttributeError:
        return None
    else:
        return command


def setup(discord_client):
    discord_client.add_cog(ErrorHandlerCog(discord_client))