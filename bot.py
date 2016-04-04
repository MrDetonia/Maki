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
import random
import json
import markov

# file in this directory called "secret.py" should contain these variables
from secret import email,pwd


# CONFIGURATION

# reported bot name
name = "Maki"

# bot version
version = "v0.10.5"

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
.markov <user> - generate sentence using markov chains over a user's chat history
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
        # response to send to channel
        response = ''

        # send any messages we have for author:
        if message.author.name in tells:
            for msg in tells[message.author.name]:
                for attempt in range(5):
                    try:
                        yield from client.send_message(message.author, msg[0] + ' says "' + msg[1] + '"')
                    except discord.errors.HTTPException:
                        continue
                    else:
                        break
                else:
                    print('ERROR: Failed to send private message after 5 attempts')

            # delete this user's entry
            del tells[message.author.name]

            # update messages
            with open('tells.json', 'w') as fp:
                json.dump(tells, fp)

        # parse messages for commands
        if message.content.startswith('.bots') or message.content.startswith('.version'):
            # print bot info
            response = 'I am ' + name + ', a Discord bot by MrDetonia | ' + version + ' | Python 3.4 | discord.py ' + discord.__version__

        elif message.content.startswith('.help'):
            # print command list
            response = helptext

        elif message.content.startswith('.upskirt'):
            # link to source code
            response = 'No, don\'t look at my pantsu! Baka! <https://27b-a.xyz:55555/mrdetonia/Maki>'

        elif message.content.startswith('.die'):
            if message.author.id in admins:
                # exit discord and kill bot
                yield from client.send_message(message.channel, 'But will I dream? ;_;')
                yield from client.logout()
            else:
                # user not admin, refuse
                response = 'Don\'t be so rude! >:('

        elif message.content.startswith('.whoami'):
            # show info about user
            response = 'User: ' + message.author.name + ' ID: ' + message.author.id + ' Discriminator: ' + message.author.discriminator + '\nAccount Created: ' + strfromdt(message.author.created_at)

        elif message.content.startswith('.whois'):
            # show info about another user
            tmp = message.content[7:]
            if tmp in users:
                user = message.server.get_member(users[tmp])
                response = 'User: ' + user.name + ' ID: ' + user.id + ' Discriminator: ' + user.discriminator + '\nAccount Created: ' + strfromdt(user.created_at)
            else:
                response = 'I haven\'t seen ' + tmp + ' yet! :('

        elif message.content.startswith('.welcome'):
            # manage welcome messages
            if message.author.id in admins:
                tmp = message.content[9:].split(' ',1)
                welcomes[tmp[0]] = tmp[1]
                response = 'Okay, I will now greet ' + tmp[0] + ' with "' + tmp[1] + '"'
            else:
                welcomes[message.author.name] = message.content[9:]
                response = 'Okay, I will now greet ' + message.author.name + ' with "' + message.content[9:] + '"'

            # save welcomes
            with open('welcomes.json', 'w') as fp:
                json.dump(welcomes, fp)

        elif message.content.startswith('.seen'):
            # print when user was last seen
            target = message.content[6:]
            if target in history:
                # user logged, print last message and time
                response = 'user ' + target + ' was last seen saying "' + history[target][0] + '" at ' + strfromdt(dtfromts(history[target][1]))
            elif target == 'Maki':
                # Maki doesn't need to be .seen
                response = 'I\'m right here!'
            else:
                # user not logged
                response = 'user not seen yet'

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
            response = 'Okay ' + message.author.name + ', I\'ll tell ' + tmp[0] + ' when I next see them!'

        elif message.content.startswith('.say'):
            # delete calling message for effect
            yield from client.delete_message(message)
            # echo message
            response = message.content[5:]

        elif message.content.startswith('.markov'):
            # generate a markov chain sentence based on the user's chat history
            tmp = message.content[8:]
            if os.path.isfile('./markovs/' + users[tmp]):
                mc = markov.Markov(open('./markovs/' + users[tmp]))
                try:
                    response = mc.generate_text(random.randint(20,40))
                except KeyError:
                    response = 'Something went wrong :( Maybe you haven\'t spoken enough yet?'
            else:
                response = 'I haven\'t seen that user speak yet!'

        # Stuff that happens when message is not a bot command:
        else:
            # log each message against users
            history[message.author.name] = (message.content, time.time())
            with open('hist.json', 'w') as fp:
                json.dump(history, fp)

            # log user messages for markov chains, ignoring messages with certain substrings
            filters = ['```', 'http://', 'https://']
            if not any(x in message.content for x in filters):
                with open('./markovs/' + message.author.id, 'a') as fp:
                    fp.write('\n' + message.content)

        # Ben meme trackers
        if '/ck/' in message.content and message.author.name == "Ben.H":
            bentrack['ck'] += 1
            response = 'I have seen Ben reference /ck/ ' + str(bentrack['ck']) + ' times now.'
            # save count
            with open('bentrack.json', 'w') as fp:
                json.dump(bentrack, fp)

        elif '/fit/' in message.content and message.author.name == "Ben.H":
            bentrack['fit'] += 1
            response = 'I have seen Ben reference /fit/ ' + str(bentrack['fit']) + ' times now.'
            # save count
            with open('bentrack.json', 'w') as fp:
                json.dump(bentrack, fp)

        # send response to channel if needed:
        if response is not '':
            for attempt in range(5):
                try:
                    yield from client.send_message(message.channel, response)
                except discord.errors.HTTPException:
                    continue
                else:
                    break
            else:
                print('ERROR: Failed to send message to discord after 5 attempts')


# Run the client
client.run(email, pwd)
