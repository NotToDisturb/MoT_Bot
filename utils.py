import json
import os
import discord


async def do_simple_embed(context, title, description):
    embed_message = discord.Embed(title=title,
                                  description=description,
                                  color=0x52307c)
    bot_message = await context.send(embed=embed_message)
    await bot_message.add_reaction("🗑️")

    return bot_message


def message_has_reaction(message, emoji):
    for reaction in message.reactions:
        if reaction.emoji == emoji:
            return reaction
    return None


def get_direction_offset(direction):
    if direction == "back":
        return -1
    if direction == "forward":
        return 1


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Configs(metaclass=Singleton):
    configs = {}

    def __init__(self):
        for file in os.listdir("configs"):
            if file.endswith("json"):
                with open(os.path.join("configs", file), encoding="utf-8") as config:
                    self.configs[file.split(".")[0]] = json.load(config)


def get_config(config):
    return Configs().configs[config]


class MessageTracker(metaclass=Singleton):
    tracked = {}

    def track_message(self, message_id, message_data):
        self.tracked[message_id] = message_data

    def get_message(self, message_id):
        return self.tracked.get(message_id, None)

    def untrack_message(self, message_id):
        self.tracked[message_id] = None


def get_tracker():
    return MessageTracker()
