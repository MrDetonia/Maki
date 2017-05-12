# Maki
# ----
# Discord bot by MrDetonia
#
# Copyright 2017 Zac Herd
# Licensed under BSD 3-clause License, see LICENSE.md for more info



# IMPORTS
import os
import json


# bot version
version = "v1.0.4"


# TODO: generate this on the fly and make it look acceptable
# text shown by .help command
helptext = """I am **Maki**, a Discord bot written in Python

My commands are:
**.help** | displays this text
**.info** | prints bot info
**.upskirt** | show a link to my source
**.whoami** | displays your user info
**.whois <user>** | displays another user's info
**.seen <user>** | prints when user was last seen
**.say <msg>** | say something
**.sayy <msg>** | say something a e s t h e t i c a l l y
**.markov [<user>]** | generate markov chain over chat history for you or another user
**.roll <num>d<val>** | roll x number of y sided dice
**.qr <msg>** | generate a QR code
**.np [<user>]** | fetch now playing from last.fm for you or a specific username
**.steam [<user>]** | fetch steam status for you or a specific vanityname
"""

# IDs of admin users
admins = ['116883900688629761']

# log of users' last messages and timestamps
history = {}
if os.path.isfile('hist.json'):
	with open('hist.json', 'r') as fp:
		history = json.load(fp)

# quiet modes
quiet = {}
