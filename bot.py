
# Maki
# ----
# Discord bot by MrDetonia
#
# Copyright 2017 Zac Herd
# Licensed under BSD 3-clause License, see LICENSE.md for more info



# IMPORTS
import discord
import asyncio
import os
import io
import requests
import sys
import shlex
import subprocess
import time
import datetime
import random
import re
import json
import logging

# LOCAL IMPORTS
from common import *
from helpers import *
from commands import *
from admincommands import *

# file in this directory called "secret.py" should contain these variables
from secret import token, lfmkey, steamkey


# DISCORD CLIENT INSTANCE
client = discord.Client()


# EVENT HANDLERS
# called when client ready
@client.event
@asyncio.coroutine
def on_ready():
	# info on terminal
	print('Connected')
	print('User: ' + client.user.name)
	print('ID: ' + client.user.id)

	# set "Now Playing" to print version
	game = discord.Game(name = version)
	yield from client.change_presence(game=game)


# called when message received
@client.event
@asyncio.coroutine
def on_message(msg):
	# print messages to terminal for info
	timestr = time.strftime('%Y-%m-%d-%H:%M:%S: ')
	try:
		print("{} {} - {} | {}: {}".format(timestr, msg.server.name, msg.channel.name, msg.author.name, msg.content))
	except AttributeError:
		print("{} | PRIVATE | {}: {}".format(timestr, msg.author.name, msg.content))

	# do not parse own messages or private messages
	if msg.author != client.user and type(msg.channel) is not discord.PrivateChannel:
		# log each message against users
		if msg.content != "":
			history[msg.server.id + msg.author.id] = (msg.server.id, time.time(), msg.content)
			with open('hist.json', 'w') as fp:
				json.dump(history, fp)

		# log user messages for markov chains, ignoring messages with certain substrings
		filters = ['`', 'http://', 'https://']
		if not any(x in msg.content for x in filters):
			try:
				with open('./markovs/' + msg.server.id + '-' + msg.author.id, 'a') as fp:
					fp.write('\n' + msg.content)
			except PermissionError: pass

		# react to stuff
		yield from makireacts(client, msg)

		# check for commands
		if msg.content.startswith(prefix):
			cmd = msg.content.split(' ', 1)[0][1:]
			if cmd in commands:
				yield from commands[cmd](client, msg)
			elif cmd in admincommands and msg.author.id in admins:
				yield from admincommands[cmd](client, msg)


# MAIN FUNCTION
def main():
	logger()
	client.run(token)
	exit(0)

if __name__ == "__main__":
	main()
