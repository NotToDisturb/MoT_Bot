import os

import discord

import sheets_utils

from dotenv import load_dotenv


load_dotenv()
SHEET_ID = os.getenv("SHEET_ID")

DISCORD_TESTER = os.getenv("DISCORD_TESTER")


async def generate_csv(discord_client, message, command, args):
    if str(message.author) == str(discord_client.user) or str(message.author) == str(DISCORD_TESTER):
        spreadsheet = sheets_utils.open_spreadsheet(SHEET_ID)
        sheets_utils.generate_spreadsheet_csv(spreadsheet)

        embed_message = discord.Embed(title="Admin",
                                      description="CSV files have been rebuilt.",
                                      color=0x52307c)
        await message.channel.send(embed=embed_message)
    else:
        embed_message = discord.Embed(title="Admin",
                                      description="Not enough permission to rebuild CSV files.",
                                      color=0x52307c)
        await message.channel.send(embed=embed_message)
