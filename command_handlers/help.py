import os

import discord

from dotenv import load_dotenv

load_dotenv()
DISCORD_PREFIX = os.getenv("DISCORD_PREFIX")
DISTURBO_ICON = os.getenv("DISTURBO_ICON")


async def help_none(discord_client, message, command, args):
    embed_message = discord.Embed(title="You seem... very lost",
                                  description="I don't really know how to help you with that! To use the `" +
                                              build_prefix("help") + "` command you must follow the structure " +
                                              "`" + build_prefix("help") + " <help option>`.\n\n"
                                              "The help options I can tell you about are:\n" +
                                              build_help_options(),
                                  color=0x52307c)
    return embed_message


async def help_all(discord_client, message, command, args):
    embed_message = discord.Embed(title="I see you need some help!",
                                  description="Let me explain how you can get the info you need. To use the `" +
                                              build_prefix("help") + "` command you must follow the structure " +
                                              "`" + build_prefix("help") + " <help option>`.\n\n"
                                              "The help options I have are:\n" +
                                              build_help_options(),
                                  color=0x52307c)
    return embed_message


async def help_info(discord_client, message, command, args):
    embed_message = discord.Embed(title=build_title("\"Info\""),
                                  description="With this command you won't really do much, " +
                                              "but I'll tell you a bit about myself!\n\n" +
                                              "Type `" + build_prefix("info") + "` to use it.",
                                  color=0x52307c)
    return embed_message


async def help_pokes(discord_client, message, command, args):
    embed_message = discord.Embed(title=build_title("\"Pokes\""),
                                  description="Stub",
                                  color=0x52307c)
    return embed_message


async def help_poke(discord_client, message, command, args):
    embed_message = discord.Embed(title=build_title("\"Poke\""),
                                  description="Stub",
                                  color=0x52307c)
    return embed_message


async def help_stories(discord_client, message, command, args):
    embed_message = discord.Embed(title=build_title("\"Stories\""),
                                  description="Stub",
                                  color=0x52307c)
    return embed_message


async def help_story(discord_client, message, command, args):
    embed_message = discord.Embed(title=build_title("\"Story\""),
                                  description="Stub",
                                  color=0x52307c)
    return embed_message


async def help_reactions(discord_client, message, command, args):
    embed_message = discord.Embed(title=build_title("\"Reactions\""),
                                  description="Stub",
                                  color=0x52307c)
    return embed_message


args_to_help = {"": help_all,
                "info": help_info,
                "pokes": help_pokes,
                "poke": help_poke,
                "stories": help_stories,
                "story": help_story,
                "reactions": help_reactions}


async def help_command(discord_client, message, command, args):
    help_func = args_to_help.get(args, help_none)
    embed_message = await help_func(discord_client, message, command, args)
    bot_message = await message.channel.send(embed=embed_message)
    await bot_message.add_reaction("🗑️")


def build_prefix(command):
    return DISCORD_PREFIX + command


def build_help_options():
    help_options = ""
    for option in args_to_help.keys():
        if option != "":
            help_options += "`" + option + "`\n"
    return help_options


def build_title(option):
    return "Help on " + option + " you say?"
