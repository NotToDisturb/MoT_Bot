from utils import get_tracker


async def is_reaction_valid(discord_client, reaction, user):
    async for reactor in reaction.users():
        if reactor == discord_client.user:
            return user != discord_client.user
    return False


async def handle_reaction(reaction, user):
    message_data = get_tracker().get_message(reaction.message.id)
    if message_data:
        await message_data["reaction_handler"].handle_reaction(reaction, user, message_data)
