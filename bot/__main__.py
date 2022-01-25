import discord
from discord.ext import commands
import json
import sqlite3
from sqlite3 import Error
from Cogs.player import PlayerUtils

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

# Load cogs
initial_extensions = [
    # "Cogs.ping",
    "Cogs.economy",
    "Cogs.stockexchange"
    # "Cogs.battleship"
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
    # for guild in bot.guilds:
    #    for channel in guild.voice_channels:
    #        bot.vchannels.append(channel.id)
    #    for channel in guild.text_channels:
    #        bot.tchannels.append(channel.id)

    PlayerUtils.load_player_json()


@bot.event
async def on_disconnect():
    print("bot disconnected")
    # SAVE USER DATA!
    PlayerUtils.save_player_json()


@bot.command(name="reload")
@commands.is_owner()
async def reload(ctx: commands.Context):
    actual_extensions.clear()
    for extension in initial_extensions:
        try:
            bot.reload_extension(extension)
        except Exception as e:
            print(f"Failed to load extension {extension} {e}")
    await ctx.send("Cogs Reloaded")


@bot.command()
@commands.is_owner()
async def save(ctx: commands.Context):
    PlayerUtils.save_player_json()
bot.run(token)
