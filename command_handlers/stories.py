import csv
import os

import discord
from dotenv import load_dotenv

import file_utils

load_dotenv()
CSV_STORY_GROUPS = os.getenv("CSV_STORY_GROUPS")
CSV_STORIES = os.getenv("CSV_STORIES")


class Group:
    def __init__(self, title):
        self.title = title
        self.stories = []


def get_story_groups():
    groups = []
    with open(file_utils.do_resources_path(CSV_STORY_GROUPS), "rt") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for line in reader:
            groups.append(Group(line["Name"]))
    return groups


def get_stories_into_groups(groups):
    with open(file_utils.do_resources_path(CSV_STORIES), "rt") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for line in reader:
            groups[int(line["Group"])].stories.append(line)


async def stories_command(discord_client, message, command, args):
    groups = get_story_groups()
    get_stories_into_groups(groups)

    description = "I do have some around here...\n"
    for group in groups:
        dash = ""
        if group.title != "":
            description += "\n**" + group.title + "**"
            dash = "- "
        for story in group.stories:
            description += "\n" + dash + "[" + story["Name"] + "](" + story["Link"] + ")"
        description += "\n"

    embed_message = discord.Embed(title="You want stories?",
                                  description=description,
                                  color=0x52307c)
    await message.channel.send(embed=embed_message)
