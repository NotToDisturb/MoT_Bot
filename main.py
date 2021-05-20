import os

from dotenv import load_dotenv
import reactions

from cogwatch import Watcher
from discord.ext.commands import Bot

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_TESTER = os.getenv("DISCORD_TESTER")
DISCORD_PREFIX = os.getenv("DISCORD_PREFIX")


discord_client = Bot(DISCORD_PREFIX)
discord_client.remove_command("help")


@discord_client.event
async def on_ready():
    watcher = Watcher(discord_client, "cogs")
    await watcher.start()
    print(f"[INFO] {discord_client.user.name} has connected to Discord!")


@discord_client.event
async def on_reaction_add(reaction, user):
    if await reactions.is_reaction_valid(discord_client, reaction, user):
        await reaction.remove(user)
        await reactions.handle_reaction(reaction, user)


for file in os.listdir("cogs"):
    if file.endswith("py"):
        discord_client.load_extension("cogs." + file.split(".")[0])
discord_client.run(DISCORD_TOKEN)
