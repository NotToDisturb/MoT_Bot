import csv
import os

from dotenv import load_dotenv
from discord.ext import commands

import file_utils
import utils
from reaction_handlers.reaction_handler import DeleteHandler

load_dotenv()
CSV_STORY_GROUPS = os.getenv("CSV_STORY_GROUPS")
CSV_STORIES = os.getenv("CSV_STORIES")


class StoriesCog(commands.Cog):
    @commands.command(name="stories")
    async def stories_command(self, ctx):
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

        message = await utils.do_simple_embed(
            context=ctx,
            title="You want stories?",
            description=description
        )
        utils.get_tracker().track_message(message.id, {
            "author": ctx.author.id,
            "reaction_handler": DeleteHandler()
        })


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


def setup(discord_client):
    discord_client.add_cog(StoriesCog(discord_client))
