import re
import discord
from discord.ext import commands
import random
import math
from Cogs.player import Player
from Cogs.player import PlayerUtils


class Economy(commands.Cog, name="Economy"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="balance",
                      aliases=["b"],
                      help="Shows your current balance of bencoins.")
    async def balance(self, ctx: commands.Context):

        p = PlayerUtils.verify_player(ctx.author)
        balance = p.get_balance()
        await ctx.send("You have {} bencoins.".format(str(balance)), reference=ctx.message)

    @commands.Cog.listener("on_message")
    @commands.guild_only()
    @commands.cooldown(10, 2, commands.BucketType.member)
    async def on_message_listener(self, message):

        if message.author == self.bot.user:
            return
        r = random.randint(0, 9)

        if r == 1:

            p = PlayerUtils.verify_player(message.author)

            p.add(1)

            notif = "Congrats, you found a bencoin! Your balance is {} bencoins".format(
                p.get_balance())

            await message.channel.send(notif)

    @commands.Cog.listener("on_reaction_add")
    @commands.guild_only()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.Member or discord.User):
        bencoin = 848319748244897794

        if reaction.emoji.id == bencoin:
            sender = PlayerUtils.verify_player(user)

            receiver = PlayerUtils.verify_player(reaction.message.author)

            if sender.get_balance() > 0:
                receiver.add(1)
                sender.add(-1)
            else:
                await reaction.remove(user)

    @commands.command(name="cointoss",
                      aliases=["toss", "ct", "t"],
                      usage="<bet>",
                      help="Enter an amount to bet for a chance to 1.25x your bet. Note: you can only gain full bencoins")
    @commands.guild_only()
    async def cointoss(self, ctx: commands.Context, bet: int):
        if not ctx.channel.name == "backroom-holocom-casino":
            return
        player = PlayerUtils.verify_player(ctx.author)
        if player.get_balance() < bet or bet < 1:
            await ctx.send("That bet is more than your net worth...", reference=ctx.message)
            return
        else:
            rand = random.randint(0, 1)
            player.add(-bet)
            if rand == 1:
                payout = math.floor(bet * 2)
                player.add(payout)
                await ctx.send("We got a winner! You gained {} bencoins.".format(payout - bet), reference=ctx.message)
            else:
                await ctx.send("Your donation to the exchange is appreciated.", reference=ctx.message)

    @cointoss.error
    async def cointoss_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("You need to enter a bet eg cointoss <bet>")

    @commands.command(name="send",
                      usage="@<user> <amount>",
                      help="Sends the user specified amount from your wallet")
    @commands.guild_only()
    async def send(self, ctx: commands.Context, target: str, amount: int):
        if amount < 0:
            return
        sender = PlayerUtils.verify_player(ctx.author)
        if sender.get_balance() < amount:
            await ctx.send("Insufficient Funds.", reference=ctx.message)

        id = re.sub("[^0-9]", "", target)
        id = int(id)
        receiver = PlayerUtils.verify_player(ctx.message.guild.get_member(id))
        receiver.add(amount)
        sender.add(-amount)
        await ctx.send("You sent {} {} bencoins!".format(receiver.get_name(), amount), reference=ctx.message)
    '''
    @commands.command(name="roll",
                      aliases=["r"],
                      usage="<4|6|8|10|12|20> <bet> <guess>",
                      help="Rolls specified dice with different returns based on selected dice if correct number is guessed. d4 = 2x (25% chance), d6 = 3x (17% chance), d8 = 4x (13% chance), d10 = 5x (10% chance), d12 = 6x (8% chance), d20 = 10x (5% chance).")
    @commands.guild_only()
    async def roll(self, ctx: commands.Context, dietype: int, bet: int, guess: int):
        if not (ctx.channel.name == "backroom-holocom-casino" or ctx.channel.name == "bot-test"):
            return
        allowed_die = [4, 6, 8, 10, 12, 20]
        p = self.get_player(ctx.author)

        if not dietype in allowed_die:
            await ctx.send("Please enter a valid die ie <4|6|8|10|12|20>")
            return
        elif p["balance"] < bet or bet < 1:
            await ctx.send("That bet is more than your net worth...")
            return
        else:

            rand = random.randint(1, dietype)
            p["balance"] -= bet

            if rand == guess:
                payout = bet * dietype//2  # floor division to keep balance an int
                p["balance"] += payout
                await ctx.send("You rolled a {}, we got a winner! You gained {} bencoins.".format(rand, payout - bet))
            else:
                await ctx.send("You rolled a {}, Your donation to the exchange is appreciated.".format(rand))
    '''
    @commands.command()
    async def hello(self, ctx: commands.Context, at=""):
        print(type(at))
        print(PlayerUtils.get_playerdict())


def setup(bot):
    bot.add_cog(Economy(bot))
