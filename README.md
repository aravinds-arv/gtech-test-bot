# Discord Demo Bot
Just a simple demo bot that I built using the [discord.py](https://discordpy.readthedocs.io/en/stable/) wrapper for the Discord API. Feel free to use it as reference or as template for building one yourself..

## Local Setup
1. Copy .env.example to a new file .env and replace the placeholder with your token
2. Replace channel IDs in main\.py with your channel IDs
3. Activate virtual environment with:

```bash
$ source venv/bin/activate
```

4. Run the bot with python as:

```bash
$ python main.py
```
5. If the script fails to run due to any missing modules delete the `venv` folder, then create a new virtual environment and reinstall requirements by typing the following commands:

```bash
$ python -m venv venv
$ pip install -r requirements.txt
```

