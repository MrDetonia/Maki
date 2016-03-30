# Maki
# ----
# Discord bot by MrDetonia
#
# Copyright 2016 Zac Herd
# Licensed under BSD 3-clause License, see LICENSE.md for more info

# IMPORTS
import discord
import asyncio
import time
import datetime
from collections import namedtuple

# file in this directory called "secret.py" should contain these variables
from secret import email,pwd


# CONFIGURATION

# reported bot name
name = "Maki"

# bot version
version = "v0.4"

# text shown by .help command
helptext = """I am a bot written in Python by MrDetonia

My commands are:
```
.help - displays this text
.bots - prints basic info
.source - show a link to my source
.whoami - displays your user info
.seen <user> - prints when user was last seen
```"""

# IDs of admin users
admins = ['116883900688629761']


# GLOBALS

# number of times Ben has mentioned his meme boards
ben_ck_count = 0
ben_fit_count = 0

# log of users' last messages and timestamps
history = {'test': ('test message',time.time())}

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

        # parse messages for commands
        if message.content.startswith('.bots'):
            # print bot info
            yield from client.send_message(message.channel, 'I am ' + name + ', a Discord bot by MrDetonia | ' + version + ' | Python 3.4 with discord.py')

        elif message.content.startswith('.help'):
            # print command list
            yield from client.send_message(message.channel, helptext)

        elif message.content.startswith('.source'):
            # link to source code
            yield from client.send_message(message.channel, 'These are my insides: http://27b-a.xyz/mrdetonia/Maki')

        elif message.content.startswith('.die') and message.author.id in admins:
            # exit discord and kill bot
            yield from client.send_message(message.channel, 'y tho :(')
            yield from client.logout()
            print('exited via die command')

        elif message.content.startswith('.whoami'):
            # show info about user
            yield from client.send_message(message.channel, 'User: ' + message.author.name + ' ID: ' + message.author.id + ' Discriminator: ' + message.author.discriminator + '\nAccount Created: ' + strfromdt(message.author.created_at))

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
            ben_ck_count += 1
            yield from client.send_message(message.channel, 'I have seen Ben reference /ck/ ' + ben_ck_count + ' times now.')
        elif '/fit/' in message.content and message.author.name == "Ben.H":
            ben_ck_count += 1
            yield from client.send_message(message.channel, 'I have seen Ben reference /fit/ ' + ben_fit_count + ' times now.')

# Run the client
client.run(email, pwd)
