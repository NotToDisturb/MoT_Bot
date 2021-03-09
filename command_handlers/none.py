import os

from dotenv import load_dotenv

import message_utils

load_dotenv()
DISCORD_PREFIX = os.getenv("DISCORD_PREFIX")


async def none_command(discord_client, message, command, args):
    await message_utils.do_simple_embed(channel=message.channel,
                                        title="I didn't quite catch that",
                                        description="The command `" + DISCORD_PREFIX + command + "` doesn't exist! " +
                                                    "Use `" + DISCORD_PREFIX + "help` to get some assistance.")
    return
