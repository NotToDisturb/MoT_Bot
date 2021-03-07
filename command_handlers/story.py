import csv
import os
import re

import discord
from dotenv import load_dotenv

import file_utils
import message_utils

load_dotenv()
CSV_STORY_GROUPS = os.getenv("CSV_STORY_GROUPS")
CSV_STORIES = os.getenv("CSV_STORIES")

quotations_re = re.compile("^\"[a-zA-Z0-9 ]*\"( |$)")
name_extract_re = re.compile("(?<=\")[a-zA-Z0-9 ]*(?=\")")


async def story_command(discord_client, message, command, args):
    story_search = quotations_re.match(args)                    # Find the story's name inside "args"

    # STORY ARGUMENT NOT FOUND
    # Show error message and exit
    if not story_search:
        await message_utils.do_simple_embed(channel=message.channel,
                                            title="I didn't quite catch that",
                                            description="Try putting the story you want inside quotation marks.")
        return

    name_raw = story_search.group(0)
    args = args.replace(name_raw, "")                           # Remove story argument
    args_list = [] if args == "" else args.split(" ")           # Split args by spaces
    name_search = name_extract_re.search(name_raw)              # Match the name in between the quotations
    name = name_search.group(0)

    # INCORRECT PART ARGUMENT FORMAT
    # Show error message and exit
    if len(args_list) > 0 and not args_list[0].isnumeric():
        await message_utils.do_simple_embed(channel=message.channel,
                                            title="I didn't quite catch that",
                                            description="Are you sure you put in a part number?")
        return

    # CORRECT OR NO PART ARGUMENT
    # Obtain the part to be displayed
    if len(args_list) > 0 and args_list[0].isnumeric():         # Part argument found and has correct format
        part = int(args_list[0]) - 1
    else:                                                       # Part argument not found
        part = 0

    line, index = file_utils.find_item_in_columns_and_get_row(CSV_STORIES, "Name", name)

    # STORY NOT FOUND IN CSV
    # Show error message and exit
    if index == -1:
        await message_utils.do_simple_embed(channel=message.channel,
                                            title="I have some bad news...",
                                            description=args + " doesn't sound like any story I know.")
        return

    # Story found in CSV, proceed normally
    parts = int(line["Parts"])

    # INVALID PART
    # Show error message and exit
    if part >= parts:
        await message_utils.do_simple_embed(channel=message.channel,
                                            title="Huh, there's a problem",
                                            description="I do know \"" + line["Name"]
                                                        + "\" but it doesn't have that many parts.")
        return

    # EVERYTHING CORRECT
    # Create embedded message and add corresponding reactions
    embed_message = story_do_embed(line, part)
    bot_message = await message.channel.send(embed=embed_message)
    await story_do_reactions(bot_message, parts, part)


def story_do_embed(line, part):
    embed_message = discord.Embed(title="Story time!",
                                  description="",
                                  color=0x52307c)

    embed_message.add_field(name=line["Name"] + " - Part " + str(part + 1),
                            value="```" + story_do_read(line, part) + "```",
                            inline=False)

    group, others = story_do_on_group(line)
    if group:
        embed_message.add_field(name="\nThis story belongs to the " + group + " saga.",
                                value="__Other stories in the saga:__\n" + others,
                                inline=False)

    embed_message.set_footer(text="Written by " + line["Author"],
                             icon_url=line["Icon"])

    return embed_message


def story_get_all_in_group(line):
    other_stories = []
    with open(file_utils.do_resources_path(CSV_STORIES), "rt") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for other_line in reader:
            # The group must be the same in the fetched line and the provided one
            # and the name of the story different to the name of the provided one
            if other_line["Group"] == line["Group"] and other_line["Name"] != line["Name"]:
                other_stories.append(other_line)
    return other_stories


def story_do_on_group(line):
    group_line = file_utils.get_line_at_row(CSV_STORY_GROUPS, int(line["Group"]))
    if group_line["Name"] == "":                                # The group this story belongs to does not have a name
        return None, None
    else:
        others_list = story_get_all_in_group(line)
        others = ""
        for other in others_list:
            others = "[" + other["Name"] + "](" + other["Link"] + ")" + "\n"
        return group_line["Name"], others


def story_do_read(line, part):
    story = open(file_utils.do_resources_path(line["File"]), "rt", encoding="utf8")
    return story.read().split("|")[part]


async def story_do_reactions(message, parts, part):
    if part > 0:
        await message.add_reaction("◀️")
    if part < parts - 1:
        await message.add_reaction("▶️")
    await message.add_reaction("🗑️")
