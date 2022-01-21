import discord
from discord.ext import commands
import json
import sqlite3
from sqlite3 import Error

# Get configuration.json
with open("configuration.json", "r") as config:
    data = json.load(config)
    token = data["token"]
    prefix = data["prefix"]


# Intents
intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.reactions = True


bot = commands.Bot(prefix, intents=intents)
vchannels = []
tchannels = []

# Load cogs
initial_extensions = [
    # "Cogs.ping",
    "Cogs.economy"
]

actual_extensions = []

# Create db connection


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            print("closing db connection")
            conn.close()


if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
            actual_extensions.append(extension)
        except Exception as e:
            print(f"Failed to load extension {extension} {e}")
    # create_connection(r".\sqlite\sqlite.db")


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{bot.command_prefix}help"))
    print("Api Version: " + discord.__version__)
    print("Currently loaded extensions: " + str(actual_extensions))
    for guild in bot.guilds:
        for channel in guild.voice_channels:
            vchannels.append(channel.id)
        for channel in guild.text_channels:
            tchannels.append(channel.id)
    # print(vchannels)
    # print(tchannels)

    with open('data.json', "r") as jfile:
        data = json.load(jfile)
        bot.players = data
        print(bot.players)


@bot.event
async def on_disconnect():
    print("bot disconnected")
    # SAVE USER DATA!


bot.run(token)
