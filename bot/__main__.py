import discord
from discord.ext import commands
import json
from Cogs.player import PlayerUtils

# Get configuration.json
with open("configuration.json", "r") as config:
    data = json.load(config)
    token = data["token"]
    prefix = data["prefix"]


# Intents
intents = discord.Intents.all()


bot = commands.Bot(prefix, intents=intents)

# Load cogs
initial_extensions = [
    # "Cogs.ping",
    "Cogs.events",
    "Cogs.economy",
    "Cogs.stockexchange",
    "Cogs.cargobay"
    # "Cogs.battleship"
]

actual_extensions = []

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
            actual_extensions.append(extension)
        except Exception as e:
            print(f"Failed to load extension {extension} {e}")


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


@bot.command(name="reload", hidden=True)
@commands.is_owner()
async def reload(ctx: commands.Context):
    actual_extensions.clear()
    for extension in initial_extensions:
        try:
            bot.reload_extension(extension)
        except Exception as e:
            print(f"Failed to load extension {extension} {e}")
    await ctx.send("Cogs Reloaded")


@bot.command(hidden=True)
@commands.is_owner()
async def save(ctx: commands.Context):
    PlayerUtils.save_player_json()
bot.run(token)
