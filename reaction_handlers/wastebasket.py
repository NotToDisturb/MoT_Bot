async def wastebasket_reaction(reaction, user):
    await reaction.message.delete()
