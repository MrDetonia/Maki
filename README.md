# Maki - Discord bot written in Python
### The discord bot that does things.

---

## Running Maki
Maki relies on Python 3.4+ and the latest discord.py version.  
A Dockerfile exists to handle these requirements automatically. Use `build.sh` to create the maki container image, and `run.sh` to start the bot.  
Be sure to have created `secret.py` with the required tokens before running `build.sh`.

If you would prefer not to use docker, ensure you have at least Python 3.4, and use `pip install -r requirements.txt` to install the required Python libraries. Then run `bot.py`.

## Required Files
- You will require a Discord Application for Maki to use, the token for which should be stored in a file called secret.py:
```python
token = '<Discord Application Token>'
lfmkey = '<last.fm API key>'
steamkey = '<Steam API key>'
```
- Maki uses JSON files to store data persistently. These will be created automatically in the `persist` directory.

## License
Copyright 2019, Zac Herd.  
All Rights Reserved.  
Licensed under the BSD 3-clause License.  
See LICENSE.md for a full copy of the license text.  
