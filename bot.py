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

# file in this directory called "secret.py" should contain these variables
from secret import email,pwd


# CONFIGURATION

# reported bot name
name = "Maki"

# bot version
version = "v0.9.4"

# text shown by .help command
helptext = """I am a bot written in Python by MrDetonia

My commands are:
```
.help - displays this text
.bots - prints bot info
.version - prints bot info
.upskirt - show a link to my source
.whoami - displays your user info
.whois <user> - displays another user's info
.welcome <message> - set your own welcome message
.seen <user> - prints when user was last seen
.tell <user> <message> - send message to user when they are next active
.say <msg> - say something
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
history = {}
if os.path.isfile('hist.json'):
    with open('hist.json', 'r') as fp:
        history = json.load(fp)

# user welcome messages
welcomes = {}
if os.path.isfile('welcomes.json'):
    with open('welcomes.json', 'r') as fp:
        welcomes = json.load(fp)

# seen users and IDs
users = {}
if os.path.isfile('users.json'):
    with open('users.json', 'r') as fp:
        users = json.load(fp)

# messages left for users
tells = {}
if os.path.isfile('tells.json'):
    with open('tells.json', 'r') as fp:
        tells = json.load(fp)

# this instance of the Discord client
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

    # track usernames and IDs:
    if after.name not in users:
        # store user ID
        users[after.name] = after.id

        # delete old entry if username changed
        if after.name != before.name:
            try:
                users.pop(before.name, None)
            except KeyError:
                pass

        # update JSON file
        with open('users.json', 'w') as fp:
            json.dump(users, fp)

# called when message received
@client.event
@asyncio.coroutine
def on_message(message):
    # print messages to terminal for info
    print(message.author.name + ': ' + message.content)

    # ensure we store this user's ID
    if message.author.name not in users:
        users[message.author.name] = message.author.id

        # update JSON file
        with open('users.json', 'w') as fp:
            json.dump(users, fp)

    # do not parse own messages or private messages
    if message.author != client.user and type(message.channel) is not discord.PrivateChannel:

        # send any messages we have for author:
        if message.author.name in tells:
            yield from client.send_message(message.channel, 'Hey ' + message.author.name + ', I have messages for you!')
            for msg in tells[message.author.name]:
                yield from client.send_message(message.author, msg[0] + ' says "' + msg[1] + '"')

            # delete this user's entry
            del tells[message.author.name]

            # update messages
            with open('tells.json', 'w') as fp:
                json.dump(tells, fp)

        # parse messages for commands
        if message.content.startswith('.bots') or message.content.startswith('.version'):
            # print bot info
            yield from client.send_message(message.channel, 'I am ' + name + ', a Discord bot by MrDetonia | ' + version + ' | Python 3.4 | discord.py ' + discord.__version__)

        elif message.content.startswith('.help'):
            # print command list
            yield from client.send_message(message.channel, helptext)

        elif message.content.startswith('.upskirt'):
            # link to source code
            yield from client.send_message(message.channel, 'No, don\'t look at my pantsu! Baka! <https://27b-a.xyz:55555/mrdetonia/Maki>')

        elif message.content.startswith('.die'):
            if message.author.id in admins:
                # exit discord and kill bot
                yield from client.send_message(message.channel, 'But will I dream? ;_;')
                yield from client.logout()
            else:
                # user not admin, refuse
                yield from client.send_message(message.channel, 'Don\'t be so rude! >:(')

        elif message.content.startswith('.whoami'):
            # show info about user
            yield from client.send_message(message.channel, 'User: ' + message.author.name + ' ID: ' + message.author.id + ' Discriminator: ' + message.author.discriminator + '\nAccount Created: ' + strfromdt(message.author.created_at))

        elif message.content.startswith('.whois'):
            # show info about another user
            tmp = message.content[7:]
            if tmp in users:
                user = message.server.get_member(users[tmp])
                yield from client.send_message(message.channel, 'User: ' + user.name + ' ID: ' + user.id + ' Discriminator: ' + user.discriminator + '\nAccount Created: ' + strfromdt(user.created_at))
            else:
                yield from client.send_message(message.channel, 'I haven\'t seen ' + tmp + ' yet! :(')

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
            elif target == 'Maki':
                # Maki doesn't need to be .seen
                yield from client.send_message(message.channel, 'I\'m right here!')
            else:
                # user not logged
                yield from client.send_message(message.channel, 'user not seen yet')

        elif message.content.startswith('.tell'):
            # store message to tell user
            tmp = message.content[6:].split(' ',1)
            try:
                tells[tmp[0]].append((message.author.name, tmp[1]))
            except (NameError, KeyError):
                tells[tmp[0]] = [(message.author.name, tmp[1])]

            # save messages
            with open('tells.json', 'w') as fp:
                json.dump(tells, fp)

            # let user know message is ready
            yield from client.send_message(message.channel, 'Okay ' + message.author.name + ', I\'ll tell ' + tmp[0] + ' when I next see them!')

        elif message.content.startswith('.say'):
            # delete calling message for effect
            yield from client.delete_message(message)
            # echo message
            yield from client.send_message(message.channel, message.content[5:])

        else:
            # log each message against users
            history[message.author.name] = (message.content, time.time())
            with open('hist.json', 'w') as fp:
                json.dump(history, fp)

        # Ben meme trackers
        if '/ck/' in message.content and message.author.name == "Ben.H":
            bentrack['ck'] += 1
            yield from client.send_message(message.channel, 'I have seen Ben reference /ck/ ' + str(bentrack['ck']) + ' times now.')
            # save count
            with open('bentrack.json', 'w') as fp:
                json.dump(bentrack, fp)

        elif '/fit/' in message.content and message.author.name == "Ben.H":
            bentrack['fit'] += 1
            yield from client.send_message(message.channel, 'I have seen Ben reference /fit/ ' + str(bentrack['fit']) + ' times now.')
            # save count
            with open('bentrack.json', 'w') as fp:
                json.dump(bentrack, fp)


# Run the client
client.run(email, pwd)
