# Maki
# ----
# Discord bot by MrDetonia
#
# Copyright 2018 Zac Herd
# Licensed under BSD 3-clause License, see LICENSE.md for more info

# IMPORTS
import asyncio
import discord
import logging
import datetime
import re

# LOCAL IMPORTS
from common import *


# clamps an integer
def clamp(n, small, large):
    return max(small, min(n, large))


# converts a datetime to a string
def strfromdt(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')


# converts a timestamp to a datetime
def dtfromts(ts):
    return datetime.datetime.fromtimestamp(ts)


# logging setup
def logger():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(
        filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(
        logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)


# send_message wrapper (deals with Discord's shit API)
@asyncio.coroutine
def discord_send(client, message, response):
    if response is not '' and message.server.id not in quiet:
        for attempt in range(5):
            try:
                yield from client.send_message(message.channel, response)
            except discord.errors.HTTPException:
                continue
            else:
                break
        else:
            print('ERROR: Failed to send message to discord after 5 attempts')


# send typing signal to Discord
@asyncio.coroutine
def discord_typing(client, message):
    for attempt in range(5):
        try:
            yield from client.send_typing(message.channel)
        except discord.errors.HTTPException:
            continue
        else:
            break
    else:
        print(
            'ERROR: Failed to send typing signal to discord after 5 attempts')


# Maki Reacts to...
@asyncio.coroutine
def makireacts(client, msg):
    # TODO: track down the person(s) responsible for naming emoji
    reactions = {
        r"\bmaki\b": "\N{BLACK HEART SUIT}",
        r"\bbutter\b": "\N{PERSON WITH FOLDED HANDS}",
        r"\begg[s]?\b": "\N{AUBERGINE}",
        r"\bproblematic\b": "\N{EYEGLASSES}",
    }

    for i in reactions:
        if bool(re.search(i, msg.content, re.IGNORECASE)):
            yield from client.add_reaction(msg, reactions[i])
