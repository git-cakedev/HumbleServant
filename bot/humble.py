from player import Player
import discord
from discord.ext import commands
import os
import json
import datetime

# change other's nickname for an hour
# bencoin reacts give sender a coin
# .imtrapped posts a pic of a trap

bot = commands.Bot(command_prefix=".")

try:
    TOKEN = os.environ["DISCORD_TOKEN"]
    GUILD = os.environ["DISCORD_GUILD"]
except:
    print("DISCORD_TOKEN and/or DISCORD_GUILD environment variables not found!")
    raise discord.DiscordException


@bot.event
async def on_ready():

    print(GUILD)
    print(bot.guilds)
    # guilds = discord.utils.find(lambda g:  g.name == GUILD, bot.guilds)

    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("Listening to .help"))

    print(
        f'{bot.user.name} is connected to the following guild:\n'
        # f'{guild.name} (id: {guild.id})'
    )


@bot.command(help="PONG!")
async def ping(ctx):
    await ctx.send(f"🏓 Pong with {str(round(bot.latency, 2))}")


@bot.command(help="Who sent this message?")
async def whoami(ctx):
    await ctx.send(f"You are {ctx.message.author.name}")


@bot.command(help="clears the last 2 messages. FOR TEST PURPOSES")
async def clear(ctx, amount=3):
    await ctx.channel.purge(limit=amount)


@bot.command(help="adds two numbers separated by spaces")
async def add(ctx, a: int, b: int):
    await ctx.send(a + b)


@bot.command()
@commands.has_role("Archduke of Celibacy")
async def init(ctx):
    data = {
        "id": ctx.message.author,
        "name": ctx.message.author.name,
        "accounts": []
    }
    print(data)
    user = Player(data)
    data["accounts"].append(user.add_account())
    print(data)


@ bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


bot.run(TOKEN)
