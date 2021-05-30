import os
import discord
import datetime

from discord.ext import commands
from dotenv import load_dotenv

# change other's nickname for an hour
# bencoin reacts give sender a coin

client = commands.Bot(command_prefix=".")

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    await client.change_presence(status=discord.Status.idle, activity=discord.Game("Listening to .help"))

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name} (id: {guild.id})'
    )


@client.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong with {str(round(client.latency, 2))}")


@client.command(name="whoami")
async def whoami(ctx):
    await ctx.send(f"You are {ctx.message.author.name}")


@client.command()
async def clear(ctx, amount=3):
    await ctx.channel.purge(limit=amount)


# def maxVote(sequence):
#     if not sequence:
#         raise ValueError('empty sequence')
#     maximum = sequence[0]
#     for item in sequence:
#         if item[1] > maximum[1]:
#             maximum = item
#     return maximum

# @client.event
# async def on_reaction_add(reaction, user):
#     nested = [reaction.message, reaction.count]
#     c = 0
#     if len(votes) == 0:
#         votes.append(nested)
#         print("Poll Started")
#     else:
#         for options in votes:
#             if options[0] == reaction.message and options[1] < reaction.count:
#                 i = votes.index(options)
#                 votes[i] = nested
#                 print("Vote Updated")
#                 print(votes[i][1])
#             if reaction.message not in options:
#                 c = c+1
#         if c == len(votes):
#             votes.append(nested)
#             print("Vote Added")


# @client.event
# async def on_raw_reaction_remove(payload):
#     msgid = payload.message_id

#     for j in votes:
#         if j[0].id == msgid:
#             index = votes.index(j)
#             votes[index][1] = int(votes[index][1] - 1)
#             print("Vote Removed")


# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     # change this to be time based?
#     if message.content.startswith('!movienight'):
#         x = datetime.datetime.today()
#         print(x)
#         votes.clear()
#         print("votes cleared")

#         if x.weekday() == 2 or x.weekday() == 5:
#             #            roleId = int(825420088677105665)
#             role = discord.utils.get(message.guild.roles, name="MovieNight")
#             try:
#                 msg = "{} it's movie night, put your selected film up".format(
#                     role.mention)
#             except:
#                 msg = "it's movie night, put your selected film up"
#             await message.channel.send(msg)  # send first announcment
#         else:
#             await message.channel.send("Tonight's not movie night :(")

#     if message.content.startswith('!callvote'):
#         win = maxVote(votes)
#         w = win[0]

#         await message.channel.send("@MovieNight The winning movie is:")
#         try:
#             f = await w.attachments[0].to_file()
#             await message.channel.send(file=f, embed=discord.Embed())
#         except:
#             await message.channel.send(w.content)
#         print(w.content)

client.run(TOKEN)
