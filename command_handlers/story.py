import csv
import os

import discord
from dotenv import load_dotenv

import file_utils

load_dotenv()
CSV_STORY_GROUPS = os.getenv("CSV_STORY_GROUPS")
CSV_STORIES = os.getenv("CSV_STORIES")


async def story_command(discord_client, message, command, args):
    line, index = file_utils.find_item_in_columns_and_get_row(CSV_STORIES, "Name", args)
    if index > -1:
        # group_line = file_utils.get_line_at_row(CSV_STORY_GROUPS, int(line["Group"]))

        embed_message = story_do_embed(line, 0)

        bot_message = await message.channel.send(embed=embed_message)
        await story_do_reactions(bot_message, line, 0)
    else:
        embed_message = discord.Embed(title="I have some bad news...",
                                      description=args + " doesn't sound like any story I know.",
                                      color=0x52307c)
        bot_message = await message.channel.send(embed=embed_message)
        await bot_message.add_reaction("🗑️")


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


def story_get_from_group(line):
    other_stories = []
    with open(file_utils.do_resources_path(CSV_STORIES), "rt") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for other_line in reader:
            if other_line["Group"] == line["Group"] and other_line["Name"] != line["Name"] :
                other_stories.append(other_line)
    return other_stories


def story_do_on_group(line):
    group_line = file_utils.get_line_at_row(CSV_STORY_GROUPS, int(line["Group"]))
    if group_line["Name"] == "":
        return None, None
    else:
        others_list = story_get_from_group(line)
        others = ""
        for other in others_list:
            others = "[" + other["Name"] + "](" + other["Link"] + ")" + "\n"
        return group_line["Name"], others


def story_do_read(line, part):
    story = open(file_utils.do_resources_path(line["File"]), "rt", encoding="utf8")
    return story.read().split("|")[part]


async def story_do_reactions(message, story_line, part_index):
    if part_index > 0:
        await message.add_reaction("◀️")
    if part_index < int(story_line["Parts"]) - 1:
        await message.add_reaction("▶️")
    await message.add_reaction("🗑️")
