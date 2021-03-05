from reaction_handlers.wastebasket import wastebasket_reaction
from reaction_handlers.back import back_reaction
from reaction_handlers.forward import forward_reaction


async def is_reaction_valid(discord_client, reaction, user):
    has_bot = False
    async for reactor in reaction.users():
        if reactor == discord_client.user:
            has_bot = True
            break

    return user != discord_client.user and has_bot


reaction_to_func = {"🗑️": wastebasket_reaction,
                    "◀️": back_reaction,
                    "▶️": forward_reaction}


async def handle_reaction(reaction, user):
    await reaction_to_func.get(reaction.emoji)(reaction, user)
