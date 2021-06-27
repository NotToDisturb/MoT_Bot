import utils


class ReactionHandler:
    reaction_to_function = {}

    def __init__(self, do_embed=None):
        self.build_embed = do_embed

    async def handle_reaction(self, reaction, user, message_data):
        if user.id == message_data["author"]:
            function = self.reaction_to_function.get(reaction.emoji, None)
            if function:
                await function(self, reaction, user, message_data)


class DeleteHandler(ReactionHandler):
    async def handle_wastebasket(self, reaction, user, message_data):
        utils.get_tracker().untrack_message(user.id)
        await reaction.message.delete()

    reaction_to_function = {"🗑️": handle_wastebasket}


class SideArrowsHandler(ReactionHandler):
    async def handle_wastebasket(self, reaction, user, message_data):
        utils.get_tracker().untrack_message(user.id)
        await reaction.message.delete()

    async def handle_left_arrow(self, reaction, user, message_data):
        await self.handle_directional_arrow(reaction, user, message_data, -1)

    async def handle_right_arrow(self, reaction, user, message_data):
        await self.handle_directional_arrow(reaction, user, message_data, 1)

    async def handle_directional_arrow(self, reaction, user, message_data, offset):
        pass

    async def update_reactions(self, message, index, left_limit, right_limit, loop=True):
        await self.update_arrow(message, index, "◀️", left_limit, loop)
        await self.update_arrow(message, index, "▶️", right_limit, loop)

    async def update_arrow(self, message, index, emoji, compare, loop):
        reaction = utils.message_has_reaction(message, emoji)
        if not loop and index == compare and reaction:
            await reaction.clear()
        elif not reaction:
            await message.add_reaction(emoji)

    reaction_to_function = {
        "🗑️": handle_wastebasket,
        "◀️": handle_left_arrow,
        "▶️": handle_right_arrow
    }
