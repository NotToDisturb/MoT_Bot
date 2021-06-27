import os

from reaction_handlers.general_handlers import SideArrowsHandler

CSV_STORY_GROUPS = os.getenv("CSV_STORY_GROUPS")
CSV_STORIES = os.getenv("CSV_STORIES")


class StoryHandler(SideArrowsHandler):
    def __init__(self, build_embed):
        self.build_embed = build_embed

    async def handle_directional_arrow(self, reaction, user, message_data, offset):
        line = message_data["line"]
        part = message_data["part"] + offset
        parts = int(line["Parts"]) - 1
        message_data["part"] = part
        embed_message = self.build_embed((line, part), 0)
        await reaction.message.edit(embed=embed_message)

        await self.update_reactions(reaction.message, part, 0, parts, False)
