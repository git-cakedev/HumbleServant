from pydoc import describe
import discord
from discord.ext import commands
import json
import random
import math


class Economy(commands.Cog, name="Economy"):
    def __init__(self, bot):
        self.bot = bot

    async def notify(self, ctx, member: discord.Member, message: str):
        player = self.get_player(member)
        if player["blacklisted"] == True:
            return
        try:

            channel = await member.create_dm()
            await channel.send(message)
            # await ctx.send(f':white_check_mark: Your Message has been sent')
        except:
            await ctx.send(':x: Member had their dm close, message not sent')

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
            id, {"name": player.name + "#" + str(player.discriminator), "balance": 100, "blacklisted": True})
        return result

    @commands.command(name="balance",
                      aliases=["b"],
                      help="Shows your current balance of bencoins.")
    async def balance(self, ctx: commands.Context):
        balance = self.get_player(ctx.author)["balance"]
        await ctx.send("You have {} bencoins.".format(str(balance)))

    @commands.command(name="mute",
                      aliases=["blacklist"],
                      help="Toggles DM notifications from Humble Servant.")
    async def mute(self, ctx: commands.Context):
        toggle = self.get_player(ctx.author)["blacklisted"]
        if toggle == False:
            self.get_player(ctx.author)["blacklisted"] = True
        else:
            self.get_player(ctx.author)["blacklisted"] = False
        self.save_json()

    @commands.Cog.listener("on_message")
    @commands.guild_only()
    @commands.cooldown(10, 2, commands.BucketType.member)
    async def on_message_listener(self, message):

        if message.author == self.bot.user:
            return
        r = random.randint(0, 9)

        if r == 1:

            id = str(message.author.id)

            d = self.get_player(message.author)

            d["balance"] += 1
            self.bot.players[id] = d

            notif = "Congrats, you found a bencoin! Your balance is {} bencoins".format(
                d["balance"])
            self.save_json()

            if d["blacklisted"] == False:
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

                if receiver["blacklisted"] == False:
                    await self.notify(self, reaction.message.author, "{} gave you a bencoin reaction! Don't spend it all in one place! Your Balance: {}".format(user.name, receiver["balance"]))
                if sender["blacklisted"] == False:
                    await self.notify(self, user, "You gave {} a bencoin reaction! Hope it was worth it! Your Balance: {}".format(reaction.message.author.name, sender["balance"]))

            else:
                if sender["blacklisted"] == False:
                    await self.notify(self, user, "You tried to give {} a bencoin reaction but you don't have any in your wallet. Your Balance: {}".format(reaction.message.author.name, sender["balance"]))
                await reaction.remove(user)
            self.save_json()

    @commands.command(name="cointoss",
                      aliases=["toss", "ct", "t"],
                      usage="<bet>",
                      help="Enter an amount to bet for a chance to 1.25x your bet. Note: you can only gain full bencoins")
    @commands.guild_only()
    async def cointoss(self, ctx: commands.Context, bet: int):
        if not ctx.channel.name == "backroom-holocom-casino":
            return
        player = self.get_player(ctx.author)
        if player["balance"] < bet or bet < 1:
            await ctx.send("That bet is more than your net worth...")
            return
        else:
            rand = random.randint(0, 1)
            player["balance"] -= bet
            if rand == 1:
                payout = math.floor(bet * 1.25)
                player["balance"] += payout
                await ctx.send("We got a winner! You gained {} bencoins.".format(payout - bet))
            else:
                await ctx.send("Your donation to the exchange is appreciated.")

    @cointoss.error
    async def cointoss_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("You need to enter a bet eg cointoss <bet>")

    @commands.command(help="for cale use only")
    @commands.is_owner()
    async def save(self, ctx):
        return self.save_json()

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
                payout = bet * dietype//2  # floor division to keep balance as an int
                p["balance"] += payout
                await ctx.send("You rolled a {}, we got a winner! You gained {} bencoins.".format(rand, payout - bet))
            else:
                await ctx.send("You rolled a {}, Your donation to the exchange is appreciated.".format(rand))


def setup(bot):
    bot.add_cog(Economy(bot))
