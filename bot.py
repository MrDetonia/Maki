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
import io
import sys
import shlex
import subprocess
import time
import datetime
import random
import re
import json
import logging

import markov

# file in this directory called "secret.py" should contain these variables
from secret import token


# CONFIGURATION

# reported bot name
name = "Maki"

# bot version
version = "v0.16.2"

# text shown by .help command
helptext = """I am a bot written in Python by MrDetonia

My commands are:
```
.help - displays this text
.info - prints bot info
.upskirt - show a link to my source
.whoami - displays your user info
.whois <user> - displays another user's info
.seen <user> - prints when user was last seen
.say <msg> - say something
.sayy <msg> - say something a e s t h e t i c a l l y
.markov <user> - generate sentence using markov chains over a user's chat history
.roll <x>d<y> - roll x number of y sided dice
.qr <msg> - generate a QR code
```"""

# IDs of admin users
admins = ['116883900688629761']


# GLOBALS

# log of users' last messages and timestamps
history = {}
if os.path.isfile('hist.json'):
    with open('hist.json', 'r') as fp:
        history = json.load(fp)

# this instance of the Discord client
client = discord.Client()

# logging setup
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


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
    timestr = time.strftime('%Y-%m-%d-%H:%M:%S: ')
    try:
        print(timestr + message.server.name + ' ' + message.channel.name + ' ' + message.author.name + ': ' + message.content)
    except AttributeError:
        print(timestr + 'PRIV ' + message.author.name + ': ' + message.content)

    # do not parse own messages or private messages
    if message.author != client.user and type(message.channel) is not discord.PrivateChannel:
        # response to send to channel
        response = ''

        # parse messages for commands
        if message.content.startswith('.info'):
            # print bot info
            pyver = str(sys.version_info[0]) + '.' + str(sys.version_info[1]) + '.' + str(sys.version_info[2])
            response = 'I am ' + name + ', a Discord bot by MrDetonia | ' + version + ' | Python ' + pyver + ' | discord.py ' + discord.__version__

        elif message.content.startswith('.help'):
            # print command list
            response = helptext

        elif message.content.startswith('.upskirt'):
            # link to source code
            response = 'No, don\'t look at my pantsu! Baka! <https://gitla.in/MrDetonia/maki>'

        elif message.content.startswith('.die'):
            if message.author.id in admins:
                # exit discord and kill bot
                print('INFO: Accepting .die from ' + message.author.name)
                run = False
                yield from client.send_message(message.channel, 'But will I dream? ;_;')
                yield from client.logout()
            else:
                # user not admin, refuse
                response = 'Don\'t be so rude! >:('

        elif message.content.startswith('.whoami'):
            # show info about user
            response = 'User: ' + message.author.name + ' ID: ' + message.author.id + ' Discriminator: ' + message.author.discriminator + '\nAccount Created: ' + strfromdt(message.author.created_at)

        elif message.content.startswith('.whois '):
            # show info about another user
            tmp = message.content[7:]
            user = message.server.get_member_named(tmp)
            if user == None:
                response = 'I can\'t find ' + tmp
            else:
                response = 'User: ' + user.name + ' ID: ' + user.id + ' Discriminator: ' + user.discriminator + '\nAccount Created: ' + strfromdt(user.created_at)

        elif message.content.startswith('.seen '):
            # print when user was last seen
            target = message.server.get_member_named(message.content[6:]).id

            if target in history:
                # user logged, print last message and time
                response = 'user ' + message.content[6:] + ' was last seen saying "' + history[target][0] + '" at ' + strfromdt(dtfromts(history[target][1]))
            elif message.content[6:] == 'Maki':
                # Maki doesn't need to be .seen
                response = 'I\'m right here!'
            else:
                # user not logged
                response = 'user not seen yet'

        elif message.content.startswith('.say '):
            # delete calling message for effect
            yield from client.delete_message(message)
            # echo message
            response = message.content[5:]

        elif message.content.startswith('.sayy '):
            # delete calling message
            yield from client.delete_message(message)
            # echo aesthetic message
            response = ' '.join(message.content[6:])

        elif message.content.startswith('.markov '):
            # send typing signal to discord
            for attempt in range(5):
                try:
                    yield from client.send_typing(message.channel)
                except discord.errors.HTTPException:
                    continue
                else:
                    break
            else:
                print('ERROR: Failed to send typing signal to discord after 5 attempts')

            # generate a markov chain sentence based on the user's chat history
            tmp = message.content[8:]
            target = message.server.get_member_named(tmp).id
            if os.path.isfile('./markovs/' + target):
                mc = markov.Markov(open('./markovs/' + target))
                response = mc.generate_text(random.randint(20,40))
            else:
                response = 'I haven\'t seen them speak yet!'

        elif message.content.startswith('.roll '):
            # DnD style dice roll
            tmp = message.content[6:]

            #check syntax is valid
            pattern = re.compile('^([0-9]+)d([0-9]+)$')

            if pattern.match(tmp):
                # extract numbers
                nums = [int(s) for s in re.findall(r'\d+', message.content)]

                # limit range
                if nums[0] > 100: nums[0] = 100
                if nums[1] > 1000000: nums[1] = 1000000

                # roll dice multiple times and sum
                rollsum = 0
                for i in range(nums[0]):
                    rollsum += random.randint(1, nums[1])

                response = 'You rolled: ' + str(rollsum)
            else:
                response = 'you did it wrong!'

        elif message.content.startswith('.qr '):
            # generate QR code - DANGEROUS, CHECK CAREFULLY HERE
            tmp = message.content[4:]

            # send typing signal to discord
            for attempt in range(5):
                try:
                    yield from client.send_typing(message.channel)
                except discord.errors.HTTPException:
                    continue
                else:
                    break
            else:
                print('ERROR: Failed to send typing signal to discord after 5 attempts')

            # make sure there are no nasty characters
            msg = re.sub(r'[^a-zA-Z0-9_ -]', '', tmp, 0)

            # echo message
            cmd = 'echo "\'' + msg + '\'"'
            args = shlex.split(cmd)
            echo = subprocess.Popen(args, stdout=subprocess.PIPE)

            # generate QR code
            cmd = 'qrencode -t png -o -'
            args = shlex.split(cmd)
            qr = subprocess.Popen(args, stdin=echo.stdout, stdout=subprocess.PIPE)

            # upload file with curl and get URL
            cmd = 'curl -F upload=@- https://w1r3.net'
            args = shlex.split(cmd)
            out = subprocess.check_output(args, stdin=qr.stdout)

            # run piped commands
            echo.wait()

            # send response
            response = out.decode('utf-8').strip()

        # Stuff that happens when message is not a bot command:
        else:
            # log each message against users
            if message.content != "":
                history[message.author.id] = (message.content, time.time())
                with open('hist.json', 'w') as fp:
                    json.dump(history, fp)

            # log user messages for markov chains, ignoring messages with certain substrings
            filters = ['```', 'http://', 'https://']
            if not any(x in message.content for x in filters):
                with open('./markovs/' + message.author.id, 'a') as fp:
                    fp.write('\n' + message.content)

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
client.run(token)

# finish execution
exit(0)
