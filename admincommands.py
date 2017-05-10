# Maki
# ----
# Discord bot by MrDetonia
#
# Copyright 2017 Zac Herd
# Licensed under BSD 3-clause License, see LICENSE.md for more info



# IMPORTS
import os
import asyncio
import subprocess
import discord


# LOCAL IMPORTS
from common import *
from helpers import *



# COMMAND IMPLEMENTATINS
@asyncio.coroutine
def cmd_die(client, msg):
	print("INFO: accepting .die from " + msg.author.name)
	yield from client.send_message(msg.channel, "But will I dream? ;-;")
	yield from client.logout()

	if msg.content[5:] == "reload":
		# touch file to signal reload
		with open("reload", "a"):
			os.utime("reload", None)


@asyncio.coroutine
def cmd_quiet(client, msg):
	quiet[msg.server.id] = 1


@asyncio.coroutine
def cmd_loud(client, msg):
	if msg.server.id in quiet:
		quiet.pop(msg.server.id, None)



# COMMAND HANDLING
admincommands = {
	"die": cmd_die,
	"quiet": cmd_quiet,
	"loud": cmd_loud,
}