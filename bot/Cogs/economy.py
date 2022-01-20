import discord
from discord.ext import commands
import json
import random


class Economy(commands.Cog, name="Economy"):
    def __init__(self, bot):
        self.bot = bot

    async def notify(self, ctx, member: discord.Member, message: str):

        try:

            channel = await member.create_dm()
            await channel.send(message)
            # await ctx.send(f':white_check_mark: Your Message has been sent')
        except:
            # await ctx.send(':x: Member had their dm close, message not sent')
            pass

    def save_json(self):
        with open('data.json', "w") as file:
            new_data = self.bot.players
            json.dump(new_data, file, indent=4)

    @commands.Cog.listener("on_message")
    async def on_message_listener(self, message):

        if message.author == self.bot.user:
            return
        r = random.randint(0, 29)

        if r == 1:
            print('here')
            id = str(message.author.id)

            d = self.bot.players.setdefault(id, {"name": "", "balance": 0})

            d["name"] = str(message.author)
            d["balance"] += 1
            self.bot.players[id] = d

            notif = "Your balance is {} bencoins".format(d["balance"])
            self.save_json(self)
            await self.notify(self, message.author, notif)

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
