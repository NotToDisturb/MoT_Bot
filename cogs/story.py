import csv
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands
from inspect import Parameter

import file_utils
import utils
from reaction_handlers.reaction_handler import DeleteHandler
from reaction_handlers.story_handler import StoryHandler

load_dotenv()
CSV_STORY_GROUPS = os.getenv("CSV_STORY_GROUPS")
CSV_STORIES = os.getenv("CSV_STORIES")


class StoryCog(commands.Cog):
    @commands.command(name="story")
    async def story_command(self, ctx, *args):
        if len(args) == 0:
            utils.raise_incorrect_usage()

        # INCORRECT PART ARGUMENT FORMAT
        # Show error message and exit
        if len(args) > 1 and not args[1].isnumeric():
            await do_not_a_part_number(ctx)
            return

        # CORRECT OR NO PART ARGUMENT
        # Obtain the part to be displayed
        if len(args) > 1 and args[1].isnumeric():  # Part argument found and has correct format
            part = int(args[0]) - 1
        else:  # Part argument not found
            part = 0

        line, index = file_utils.find_item_in_columns_and_get_row(CSV_STORIES, "Name", args[0])

        # STORY NOT FOUND IN CSV
        # Show error message and exit
        if index == -1:
            await do_not_a_story(ctx, args[0])
            return

        # Story found in CSV, proceed normally
        parts = int(line["Parts"])

        # INVALID PART
        # Show error message and exit
        if part >= parts:
            await do_page_too_high(ctx, line)
            return

        # EVERYTHING CORRECT
        # Create embedded message and add corresponding reactions
        embed_message = do_embed(line, part)
        message = await ctx.send(embed=embed_message)
        await add_reactions(message, parts, part)
        utils.get_tracker().track_message(message.id, {
            "author": ctx.author.id,
            "part": part,
            "line": line,
            "reaction_handler": StoryHandler(do_embed)
        })


async def do_not_a_part_number(ctx):
    message = await utils.do_simple_embed(
        context=ctx,
        title="I didn't quite catch that",
        description="Are you sure you put in a part number?"
    )
    utils.get_tracker().track_message(message.id, {
        "author": ctx.author.id,
        "reaction_handler": DeleteHandler()
    })


async def do_not_a_story(ctx, story):
    message = await utils.do_simple_embed(
        context=ctx,
        title="I have some bad news...",
        description=story + " doesn't sound like any story I know."
    )
    utils.get_tracker().track_message(message.id, {
        "author": ctx.author.id,
        "reaction_handler": DeleteHandler()
    })


async def do_page_too_high(ctx, line):
    message = await utils.do_simple_embed(
        context=ctx,
        title="Huh, there's a problem",
        description="I know " + "[\"" + line["Name"] + "\"](" + line["Link"] + ")"
                    + " but it doesn't have that many parts."
    )
    utils.get_tracker().track_message(message.id, {
        "author": ctx.author.id,
        "reaction_handler": DeleteHandler()
    })


def do_embed(line, part):
    embed_message = discord.Embed(title="Story time!",
                                  description="",
                                  color=0x52307c)

    embed_message.add_field(name=line["Name"] + " - Part " + str(part + 1),
                            value="```" + get_story_part(line, part) + "```",
                            inline=False)

    group, others = do_on_group(line)
    if group:
        embed_message.add_field(name="\nThis story belongs to the " + group + " saga.",
                                value="__Other stories in the saga:__\n" + others,
                                inline=False)

    embed_message.set_footer(text="Written by " + line["Author"],
                             icon_url=line["Icon"])

    return embed_message


def get_all_in_group(line):
    other_stories = []
    with open(file_utils.do_resources_path(CSV_STORIES), "rt") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for other_line in reader:
            # The group must be the same in the fetched line and the provided one
            # and the name of the story different to the name of the provided one
            if other_line["Group"] == line["Group"] and other_line["Name"] != line["Name"]:
                other_stories.append(other_line)
    return other_stories


def do_on_group(line):
    group_line = file_utils.get_line_at_row(CSV_STORY_GROUPS, int(line["Group"]))
    if group_line["Name"] == "":  # The group this story belongs to does not have a name
        return None, None

    others_list = get_all_in_group(line)
    others = ""
    for other in others_list:
        others = "[" + other["Name"] + "](" + other["Link"] + ")" + "\n"
    return group_line["Name"], others


def get_story_part(line, part):
    with open(file_utils.do_resources_path(line["File"]), "rt", encoding="utf8") as story:
        return story.read().split("|")[part]


async def add_reactions(message, parts, part):
    if part > 0:
        await message.add_reaction("◀️")
    if part < parts - 1:
        await message.add_reaction("▶️")
    await message.add_reaction("🗑️")


def setup(discord_client):
    discord_client.add_cog(StoryCog(discord_client))
