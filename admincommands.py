# Maki
# ----
# Discord bot by MrDetonia
#
# Copyright 2018 Zac Herd
# Licensed under BSD 3-clause License, see LICENSE.md for more info

# IMPORTS
import os
import asyncio
import subprocess
import discord
import urllib.request

# LOCAL IMPORTS
from common import *
from helpers import *


# COMMAND IMPLEMENTATINS
@asyncio.coroutine
def cmd_die(client, msg):
    print("INFO: accepting .die from " + msg.author.name)
    yield from client.send_message(msg.channel, "But will I dream? ;-;")
    yield from client.logout()


@asyncio.coroutine
def cmd_quiet(client, msg):
    quiet[msg.server.id] = 1


@asyncio.coroutine
def cmd_loud(client, msg):
    if msg.server.id in quiet:
        quiet.pop(msg.server.id, None)


@asyncio.coroutine
def cmd_avatar(client, msg):
    url = msg.content[8:]
    response = "Avatar updated!"
    try:
        httpresponse = urllib.request.urlopen(url)
        imgdata = httpresponse.read()
        yield from client.edit_profile(avatar=imgdata)
    except urllib.error.URLError as e:
        response = "URL Error: " + str(e)
    except discord.HTTPException:
        response = "Dicsord failed to edit my profile!"
    except discord.InvalidArgument:
        response = "Invalid image!"
    except:
        response = "Error updating avatar!"

    yield from discord_send(client, msg, response)


# COMMAND HANDLING
admincommands = {
    "die": cmd_die,
    "quiet": cmd_quiet,
    "loud": cmd_loud,
    "avatar": cmd_avatar,
}
