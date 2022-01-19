import discord
from discord.ext import commands
import json
import random


class Economy(commands.Cog, name="Economy"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()  # this is for making a command
    async def pingy(self, ctx):

        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}')

    @commands.Cog.listener("on_message")
    async def on_message_listener(self, message):

        if message.author == self.bot.user:
            return
        r = random.randint(0, 9)

        if r == 1:

            id = str(message.author.id)

            d = self.bot.players.setdefault(id, {"name": "", "balance": 0})

            d["name"] = str(message.author)
            d["balance"] += 1
            self.bot.players[id] = d

            await message.channel.send('Hello! '+str(message.author))

        with open('data.json', "w") as file:
            new_data = self.bot.players
            json.dump(new_data, file, indent=4)

    '''
    @commands.Cog.listener("on_message")
    async def on_message_listener(self, message):

        if message.author == self.bot.user:
            return

        if message.content.startswith('hello'):

            id = str(message.author.id)

            d = self.bot.players.setdefault(id, {"name": "", "balance": 0})

            d["name"] = str(message.author)
            d["balance"] += 1
            self.bot.players[id] = d

            await message.channel.send('Hello! '+str(message.author))

        with open('data.json', "w") as file:
            new_data = self.bot.players
            json.dump(new_data, file, indent=4)
    '''


def setup(bot):
    bot.add_cog(Economy(bot))
