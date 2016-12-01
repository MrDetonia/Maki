#!/bin/bash

# user to effectively run bot as (so we can safely run as root for pip)
puser="admin"

while :
do
    date

    echo Updating repository...
    runuser -m $puser -c 'git pull'

    # if root we can update discord.py
    if [ "$EUID" -eq 0 ]
    then
        echo Updating discord.py...
        python3 -m pip install -U https://github.com/Rapptz/discord.py/archive/master.zip#egg=discord.py[voice]
    fi

    echo Starting Maki...
    runuser -m $puser -c 'rm -f ./reload'
    runuser -m $puser -c 'python3 bot.py'

    # okay to quit if rval was not 0
    if [ ! -f ./reload ]
    then
        echo no reload file, stopping for realsies...
        exit
    fi
done

exit
