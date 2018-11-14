# Maki
# ----
# Discord bot by MrDetonia
#
# Copyright 2018 Zac Herd
# Licensed under BSD 3-clause License, see LICENSE.md for more info

# IMPORTS
import asyncio
import os
import sys
import re
import requests
import random
import subprocess

# LOCAL IMPORTS
from common import *
from helpers import *
from secret import lfmkey, steamkey
import markov


# COMMAND IMPLEMENTATIONS
@asyncio.coroutine
def cmd_help(client, msg):
    yield from discord_send(client, msg, helptext)


@asyncio.coroutine
def cmd_info(client, msg):
    pyver = "{}.{}.{}".format(sys.version_info[0], sys.version_info[1],
                              sys.version_info[2])
    appinfo = yield from client.application_info()
    response = "I am **{}**, a Discord bot by **{}** | `{}` | Python `{}` | discord.py `{}`".format(
        appinfo.name, appinfo.owner.name, version, pyver, discord.__version__)
    yield from discord_send(client, msg, response)


@asyncio.coroutine
def cmd_upskirt(client, msg):
    response = "No, don\'t look at my pantsu, baka! <https://github.com/MrDetonia/maki>"
    yield from discord_send(client, msg, response)


whoistring = "**{}#{}**: `{}`\n**Account Created:** `{}`"


@asyncio.coroutine
def cmd_whoami(client, msg):
    response = whoistring.format(msg.author.name,
                                 msg.author.discriminator, msg.author.id,
                                 strfromdt(msg.author.created_at))
    yield from discord_send(client, msg, response)


@asyncio.coroutine
def cmd_whois(client, msg):
    tmp = msg.content[7:]
    user = msg.server.get_member_named(tmp)

    if user == None:
        reponse = "I can't find `{}`".format(tmp)
    else:
        response = whoistring.format(user.name, user.discriminator, user.id,
                                     strfromdt(user.created_at))

    yield from discord_send(client, msg, response)


@asyncio.coroutine
def cmd_seen(client, msg):
    tmp = msg.content[6:]
    user = msg.server.get_member_named(tmp)

    if user == None:
        reponse = "I can't find `{}`".format(tmp)
    elif user.name == "Maki":
        reponse = "I'm right here!"
    else:
        target = msg.server.id + user.id
        if target in history and history[target][0] == msg.server.id:
            response = "**{}** was last seen saying the following at {}:\n{}".format(
                user.name, strfromdt(dtfromts(history[target][1])),
                history[target][2])
        else:
            response = "I haven't seen **{}** speak yet!".format(tmp)

    yield from discord_send(client, msg, response)


@asyncio.coroutine
def cmd_say(client, msg):
    response = msg.content[5:]
    yield from client.delete_message(msg)
    yield from discord_send(client, msg, response)


@asyncio.coroutine
def cmd_sayy(client, msg):
    response = " ".join(msg.content[6:])
    yield from client.delete_message(msg)
    yield from discord_send(client, msg, response)


@asyncio.coroutine
def cmd_markov(client, msg):
    yield from discord_typing(client, msg)

    tmp = msg.content[8:]
    target = ""

    if tmp == "Maki":
        response = "My markovs always say the same thing"
    else:
        if tmp == "":
            target = "{}-{}".format(msg.server.id, msg.author.id)
        else:
            try:
                target = "{}-{}".format(msg.server.id,
                                        msg.server.get_member_named(tmp).id)
            except AttributeError:
                reponse = "I can't find `{}`".format(tmp)

    if target != "":
        mfile = "./markovs/" + target
        if os.path.isfile(mfile):
            mc = markov.Markov(open(mfile))
            response = mc.generate_text(random.randint(20, 40))
        else:
            response = "I haven't seen `{}` speak yet.".format(tmp)

    yield from discord_send(client, msg, response)


@asyncio.coroutine
def cmd_roll(client, msg):
    tmp = msg.content[6:]

    pattern = re.compile("^(\d+)d(\d+)([+-]\d+)?$")
    pattern2 = re.compile("^d(\d+)([+-]\d+)?$")

    # extract numbers
    nums = [int(s) for s in re.findall(r"\d+", tmp)]

    if pattern.match(tmp):
        numdice = nums[0]
        diceval = nums[1]
    elif pattern2.match(tmp):
        numdice = 1
        diceval = nums[0]
    else:
        response = "Expected format: `[<num>]d<value>[{+-}<modifier>]`"
        yield from discord_send(client, msg, response)

    # extract modifier, if any
    modifier = 0
    modpattern = re.compile("^(\d+)?d(\d+)[+-]\d+$")
    if modpattern.match(tmp):
        modifier = nums[len(nums) - 1]

    # negate modifier, if necessary
    modpattern = re.compile("^(\d+)?d(\d+)[-]\d+$")
    if modpattern.match(tmp):
        modifier = -modifier

    # limit ranges
    numdice = clamp(numdice, 1, 10)
    diceval = clamp(diceval, 1, 1000)

    # roll and sum dice
    rolls = []
    for i in range(numdice):
        rolls.append(random.randint(1, diceval))

    rollsum = sum(rolls) + modifier

    # generate response text
    response = "**{} rolled:** {}d{}".format(msg.author.display_name, numdice,
                                             diceval)
    if modifier > 0:
        response += "+{}".format(modifier)
    if modifier < 0:
        response += "{}".format(modifier)

    response += "\n**Rolls:** `{}`".format(rolls)
    response += "\n**Result:** `{}`".format(rollsum)

    if rollsum - modifier == numdice * diceval:
        response += " *(Natural - confirmed `{}`)*".format(
            random.randint(1, 20))
    elif rollsum - modifier == numdice:
        response += " *(Crit fail - confirmed `{}`)*".format(
            random.randint(1, 20))

    yield from discord_send(client, msg, response)


@asyncio.coroutine
def cmd_qr(client, msg):
    tmp = msg.content[4:]

    yield from discord_typing(client, msg)

    # generate qr code
    qr = subprocess.Popen(
        "qrencode -t png -o -".split(),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)
    qr.stdin.write(tmp.encode("utf-8"))
    qr.stdin.close()
    out = subprocess.check_output(
        "curl -F upload=@- https://w1r3.net".split(), stdin=qr.stdout)

    response = out.decode("utf-8").strip()

    yield from discord_send(client, msg, response)


@asyncio.coroutine
def cmd_np(client, msg):
    tmp = msg.content[4:]

    if tmp == "":
        response = lastfm_np(msg.author.name)
    else:
        response = lastfm_np(tmp)

    print("CALLING SEND")
    yield from discord_send(client, msg, response)


@asyncio.coroutine
def cmd_steam(client, msg):
    tmp = msg.content[7:]

    if tmp == "":
        response = steamdata(msg.author.name)
    else:
        response = steamdata(tmp)

    yield from discord_send(client, msg, response)


# HELPER FUNCTIONS


# gets now playing information from last.fm
def lastfm_np(username):
    # sanitise username
    cleanusername = re.sub(r'[^a-zA-Z0-9_-]', '', username, 0)

    # fetch JSON from last.fm
    payload = {
        'format': 'json',
        'method': 'user.getRecentTracks',
        'user': cleanusername,
        'limit': '1',
        'api_key': lfmkey
    }
    r = requests.get("http://ws.audioscrobbler.com/2.0/", params=payload)

    # read json data
    np = r.json()

    # check we got a valid response
    if 'error' in np:
        return "I couldn't get last.fm data for `{}`".format(username)

    # get fields
    try:
        username = np['recenttracks']['@attr']['user']
        track = np['recenttracks']['track'][0]
        album = track['album']['#text']
        artist = track['artist']['#text']
        song = track['name']
        nowplaying = '@attr' in track
    except IndexError:
        return "It looks like `{}` hasn't played anything recently.".format(
            username)

    # grammar
    if album != "":
        albumtext = "` from the album `{}`".format(album)
    else:
        albumtext = "`"

    if nowplaying == True:
        nowplaying = " is listening"
    else:
        nowplaying = " last listened"

    # construct string
    return "{}{} to `{}` by `{}{}".format(username, nowplaying, song, artist,
                                          albumtext)


# gets general steam user info from a vanityurl name
def steamdata(vanityname):
    # sanitise username
    cleanvanityname = re.sub(r'[^a-zA-Z0-9_-]', '', vanityname, 0)

    resolveurl = 'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key='
    dataurl = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key='

    # fetch json from steam
    try:
        idresponse = requests.get(resolveurl + steamkey + '&vanityurl=' +
                                  vanityname).json()['response']
    except:
        return "I can't connect to Steam"

    # check if user was found and extract steamid
    if idresponse['success'] is not 1:
        return "I couldn't find `{}`".format(vanityname)
    else:
        steamid = idresponse['steamid']

    # fetch steam user info
    try:
        dataresponse = requests.get(dataurl + steamkey + '&steamids=' +
                                    steamid).json()['response']['players'][0]
    except:
        return "Can't find info on `{}`".format(vanityname)

    personastates = [
        'Offline', 'Online', 'Busy', 'Away', 'Snoozed', 'Looking to trade',
        'Looking to play'
    ]

    if 'personaname' in dataresponse: namestr = dataresponse['personaname']
    else: namestr = ''
    if 'personastate' in dataresponse:
        statestr = '`' + personastates[dataresponse['personastate']] + '`'
    else:
        statestr = ''
    if 'gameextrainfo' in dataresponse:
        gamestr = ' playing `' + dataresponse['gameextrainfo'] + '`'
    else:
        gamestr = ''

    responsetext = [(namestr + ' is ' + statestr + gamestr).replace('  ', ' ')]

    return '\n'.join(responsetext)


# COMMAND HANDLING
prefix = "."

commands = {
    "help": cmd_help,
    "info": cmd_info,
    "upskirt": cmd_upskirt,
    "whoami": cmd_whoami,
    "whois": cmd_whois,
    "seen": cmd_seen,
    "say": cmd_say,
    "sayy": cmd_sayy,
    "markov": cmd_markov,
    "roll": cmd_roll,
    "qr": cmd_qr,
    "np": cmd_np,
    "steam": cmd_steam,
}
