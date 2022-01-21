from pydoc import describe
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

    def verify_player(self, player: discord.Member or discord.User) -> bool:
        if not str(player.id) in self.bot.players:
            return False
        return True

    def get_player(self, player: discord.Member or discord.User):
        id = str(player.id)
        result = self.bot.players.setdefault(
            id, {"name": player.name + "#" + str(player.discriminator), "balance": 0})
        return result

    @commands.command(name="balance",
                      aliases=["b"],
                      help="Shows your current balance of bencoins")
    async def balance(self, ctx: commands.Context):
        balance = self.get_player(ctx.author)["balance"]
        await ctx.send("You have {} bencoins.".format(str(balance)))

    @commands.Cog.listener("on_message")
    @commands.guild_only()
    async def on_message_listener(self, message):

        if message.author == self.bot.user:
            return
        r = random.randint(0, 29)

        if r == 1:

            id = str(message.author.id)

            d = self.get_player(message.author)

            d["balance"] += 1
            self.bot.players[id] = d

            notif = "Your balance is {} bencoins".format(d["balance"])
            self.save_json()
            await self.notify(self, message.author, notif)

    @commands.Cog.listener("on_reaction_add")
    @commands.guild_only()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.Member or discord.User):
        bencoin = 848319748244897794

        if reaction.emoji.id == bencoin:
            sender = self.get_player(user)

            receiver = self.get_player(reaction.message.author)

            if sender["balance"] > 0:
                receiver["balance"] += 1
                sender["balance"] -= 1

                await self.notify(self, reaction.message.author, "{} gave you a bencoin reaction! Don't spend it all in one place! Your Balance: {}".format(user.name, receiver["balance"]))

                await self.notify(self, user, "You gave {} a bencoin reaction! Hope it was worth it! Your Balance: {}".format(reaction.message.author.name, sender["balance"]))

            else:
                await self.notify(self, user, "You tried to give {} a bencoin reaction but you don't have any in your wallet. Your Balance: {}".format(reaction.message.author.name, sender["balance"]))
                await reaction.remove(user)
            self.save_json()


def setup(bot):
    bot.add_cog(Economy(bot))
