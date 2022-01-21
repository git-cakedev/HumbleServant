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
            await ctx.send(':x: Member had their dm close, message not sent')
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

            id = str(message.author.id)

            d = self.bot.players.setdefault(id, {"name": "", "balance": 0})

            d["name"] = str(message.author)
            d["balance"] += 1
            self.bot.players[id] = d

            notif = "Your balance is {} bencoins".format(d["balance"])
            self.save_json()
            await self.notify(self, message.author, notif)

    @commands.Cog.listener("on_reaction_add")
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.Member or discord.User):
        bencoin = 848319748244897794

        if reaction.emoji.id == bencoin:
            sender = self.bot.players.setdefault(
                str(user.id), {"name": "", "balance": 0})

            sender_balance = sender["balance"]

            receiver = self.bot.players.setdefault(
                str(reaction.message.author.id), {"name": "", "balance": 0})
            if sender_balance > 0:
                receiver["balance"] += 1
                sender_balance -= 1

                await self.notify(self, reaction.message.author, "{} gave you a bencoin reaction! Don't spend it all in one place! Your Balance: {}".format(user.name, receiver["balance"]))

                await self.notify(self, user, "You gave {} a bencoin reaction! Hope it was worth it! Your Balance: {}".format(reaction.message.author.id, sender_balance))
                print("{} sent {} a bencoin!".format(
                    user.id, reaction.message.author.id))
            else:
                await reaction.remove(user)
            self.save_json()

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
