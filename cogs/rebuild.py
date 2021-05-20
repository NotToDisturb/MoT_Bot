import os
import discord

from dotenv import load_dotenv
from discord.ext import commands

import file_utils

load_dotenv()
DISCORD_ADMINS = os.getenv("DISCORD_ADMINS").split(",")
SHEET_ID = os.getenv("SHEET_ID")


class RebuildCog(commands.Cog):
    @commands.command(name="rebuild")
    async def rebuild_command(self, ctx):
        if str(ctx.author) not in str(DISCORD_ADMINS):
            raise commands.MissingPermissions([])
        spreadsheet = file_utils.open_spreadsheet(SHEET_ID)
        file_utils.generate_spreadsheet_csv(spreadsheet)

        embed_message = discord.Embed(title="Admin",
                                      description="CSV files have been rebuilt.",
                                      color=0x52307c)
        message = await ctx.send(embed=embed_message)
        await message.delete(delay=10)


def setup(discord_client):
    discord_client.add_cog(RebuildCog(discord_client))
