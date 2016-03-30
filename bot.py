# Maki
# ----
# Discord bot by MrDetonia
#
# Copyright 2016 Zac Herd
# Licensed under BSD 3-clause License, see LICENSE.md for more info

# IMPORTS
import discord
import asyncio
import os
import time
import datetime
import json
from collections import namedtuple

# file in this directory called "secret.py" should contain these variables
from secret import email,pwd


# CONFIGURATION

# reported bot name
name = "Maki"

# bot version
version = "v0.6.0"

# text shown by .help command
helptext = """I am a bot written in Python by MrDetonia

My commands are:
```
.help - displays this text
.bots - prints basic info
.source - show a link to my source
.whoami - displays your user info
.welcome <message> - set your welcome message
.seen <user> - prints when user was last seen
```"""

# IDs of admin users
admins = ['116883900688629761']

# default posting channel
def_chan = '116884620032606215'

# GLOBALS

# number of times Ben has mentioned his meme boards
bentrack = {'ck':0, 'fit':0}
if os.path.isfile('bentrack.json'):
    with open('bentrack.json', 'r') as fp:
        bentrack = json.load(fp)

# log of users' last messages and timestamps
history = {'test': ('test message',time.time())}
if os.path.isfile('hist.json'):
    with open('hist.json', 'r') as fp:
        history = json.load(fp)

# user welcome messages
welcomes = {'test': 'test'}
if os.path.isfile('welcomes.json'):
    with open('hist.json', 'r') as fp:
        welcomes = json.load(fp)

# this instance of a Discord client
client = discord.Client()


# FUNCTIONS

# converts a datetime to a string
def strfromdt(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')

# converts a timestamp to a datetime
def dtfromts(ts):
    return datetime.datetime.fromtimestamp(ts)

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
    yield from client.change_status(game, False)

# called when member updates
@client.event
@asyncio.coroutine
def on_member_update(before, after):
    # display welcome message if user comes online:
    if before.status == discord.Status.offline and after.status == discord.Status.online:
        if after.name in welcomes:
            # print custom welcome
            yield from client.send_message(client.get_channel(def_chan), welcomes[after.name])
        else:
            yield from client.send_message(client.get_channel(def_chan), after.name + ' is now online')

# called when message received
@client.event
@asyncio.coroutine
def on_message(message):
    # print messages to terminal for info
    print(message.author.name + ': ' + message.content)

    # do not parse own messages
    if message.author != client.user:

        # log each message against users
        history[message.author.name] = (message.content, time.time())
        with open('hist.json', 'w') as fp:
            json.dump(history, fp)

        # parse messages for commands
        if message.content.startswith('.bots'):
            # print bot info
            yield from client.send_message(message.channel, 'I am ' + name + ', a Discord bot by MrDetonia | ' + version + ' | Python 3.4 with discord.py')

        elif message.content.startswith('.help'):
            # print command list
            yield from client.send_message(message.channel, helptext)

        elif message.content.startswith('.source'):
            # link to source code
            yield from client.send_message(message.channel, 'These are my insides: <http://27b-a.xyz/mrdetonia/Maki>')

        elif message.content.startswith('.die') and message.author.id in admins:
            # exit discord and kill bot
            yield from client.send_message(message.channel, 'But will I dream? ;_;')

            # logout of Discord and exit
            yield from client.logout()

        elif message.content.startswith('.whoami'):
            # show info about user
            yield from client.send_message(message.channel, 'User: ' + message.author.name + ' ID: ' + message.author.id + ' Discriminator: ' + message.author.discriminator + '\nAccount Created: ' + strfromdt(message.author.created_at))

        elif message.content.startswith('.welcome'):
            # manage welcome messages
            if message.author.id in admins:
                tmp = message.content[9:].split(' ',1)
                welcomes[tmp[0]] = tmp[1]
                yield from client.send_message(message.channel, 'Okay, I will now greet ' + tmp[0] + ' with "' + tmp[1] + '"')
            else:
                welcomes[message.author.name] = message.content[9:]
                yield from client.send_message(message.channel, 'Okay, I will now greet ' + message.author.name + ' with "' + message.content[9:] + '"')

            # save welcomes
            with open('welcomes.json', 'w') as fp:
                json.dump(welcomes, fp)

        elif message.content.startswith('.seen'):
            # print when user was last seen
            target = message.content[6:]
            if target in history:
                # user logged, print last message and time
                yield from client.send_message(message.channel, 'user ' + target + ' was last seen saying "' + history[target][0] + '" at ' + strfromdt(dtfromts(history[target][1])))
            else:
                # user not logged
                yield from client.send_message(message.channel, 'user not seen yet')

        # Ben meme trackers
        elif '/ck/' in message.content and message.author.name == "Ben.H":
            bentrack['ck'] += 1
            yield from client.send_message(message.channel, 'I have seen Ben reference /ck/ ' + bentrack['ck'] + ' times now.')
            # save count
            with open('bentrack.json', 'w') as fp:
                json.dump(bentrack, fp)

        elif '/fit/' in message.content and message.author.name == "Ben.H":
            bentrack['fit'] += 1
            yield from client.send_message(message.channel, 'I have seen Ben reference /fit/ ' + bentrack['fit'] + ' times now.')
            # save count
            with open('bentrack.json', 'w') as fp:
                json.dump(bentrack, fp)

# Run the client
client.run(email, pwd)
