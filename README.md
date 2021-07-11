# DiscordEmailBot
This is a discord bot that autimatically pulls emails from gmail and sends a message on Discord using discord.py.

The bot sends the 5 most recent emails when running the script, checks every 5 minutes for a new email.

Needs discord.py and dotenv, can be installed with 

> pip install discord.py python-dotenv

Requires .env file in the same directory with the following variables:

>TOKEN
>CHANNEL
>EMAIL
>PASS

Run the file in the background to start the script. File can be run with

>python emailPull.py
