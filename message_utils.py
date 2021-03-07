import discord


async def do_simple_embed(channel, title, description):
    embed_message = discord.Embed(title=title,
                                  description=description,
                                  color=0x52307c)
    bot_message = await channel.send(embed=embed_message)
    await bot_message.add_reaction("🗑️")

    return bot_message
