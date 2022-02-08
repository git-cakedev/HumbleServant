import discord
from discord.ext import commands, tasks
from discord.commands import slash_command, Option
import random
import math
from Cogs.player import Player
from Cogs.player import PlayerUtils
import re


class Economy(commands.Cog, name="Economy"):

    def __init__(self, bot):
        self.bot = bot
        self.active_lottery = self.Lottery(self.bot)

    GUILD_ID = int(206125299639910402)

    @commands.slash_command(guild_ids=[GUILD_ID],
                            name="balance",
                            aliases=["b"],
                            description="Shows your current balance of bencoins.")
    async def balance(self, ctx: commands.Context):

        p = PlayerUtils.verify_player(ctx.author)
        balance = p.get_balance()
        await ctx.respond(f"You have {str(balance)} bencoins.")

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

            # await message.channel.send(notif)

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

    @commands.slash_command(guild_ids=[GUILD_ID],
                            name="cointoss",
                            aliases=["ct", "t"],
                            usage="<bet>",
                            description="Enter an amount to bet for a chance to double your bet.")
    @commands.guild_only()
    async def cointoss(self, ctx: commands.Context, bet: Option(int, "Bet Amount", min_value=1)):
        if not ctx.channel.name == "backroom-holocom-casino":
            return
        player = PlayerUtils.verify_player(ctx.author)
        if player.get_balance() < bet or bet < 1:
            await ctx.respond("That bet is more than your net worth...")
            return
        else:
            rand = random.randint(0, 1)
            player.add(-bet)
            if rand == 1:
                payout = math.floor(bet * 2)
                player.add(payout)
                await ctx.respond(f"We got a winner! You gained {payout - bet} bencoins.")
            else:
                await ctx.respond("Your donation to the exchange is appreciated.")
    '''
    @cointoss.error
    async def cointoss_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.respond("You need to enter a bet eg cointoss <bet>")
    '''
    @commands.slash_command(guild_ids=[GUILD_ID],
                            name="send",
                            usage="@<user> <amount>",
                            description="Sends the user specified amount from your wallet")
    @commands.guild_only()
    async def send(self, ctx: commands.Context, target: discord.Member, amount: Option(int, "Amount to send", min=1)):
        if amount < 0:
            return
        sender = PlayerUtils.verify_player(ctx.author)
        if sender.get_balance() < amount:
            await ctx.send("Insufficient Funds.", reference=ctx.message)

        #id = re.sub("[^0-9]", "", target)
        #id = int(id)
        #receiver = PlayerUtils.verify_player(ctx.message.guild.get_member(id))
        receiver = PlayerUtils.verify_player(target)
        receiver.add(amount)
        sender.add(-amount)
        await ctx.respond(f"You sent {target.mention} {amount} bencoins!")
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
    @commands.command(hidden=True)
    async def hello(self, ctx: commands.Context, at=""):
        print(PlayerUtils.get_playerid("CakeDev#6693"))
        print(self.bot.get_channel(934593180853207111))

    class Lottery():
        active = False
        players = []
        pool = 0
        duration = 60.0

        def __init__(self, bot):
            self.bot = bot

        async def start(self, duration: float):
            self.active = True
            self.duration = duration
            self.timer.start()
            return

        @tasks.loop(seconds=duration, count=1)
        async def timer(self):
            print("")

        @timer.after_loop
        async def stop(self):
            token_list = []
            for player in self.players:
                name = player[0]
                total = player[1]

                while total > 0:
                    token_list.append([name, 1])
                    total -= 1
                    self.pool += 1

            rand = random.choice(token_list)[0]

            self.payout(rand, self.pool)
            channel = self.bot.get_channel(934593180853207111)
            winner = rand.get_name()
            print("here")
            await channel.send(f"The winner is {winner} with a total of {self.pool} bencoins!")
            print("done")
            self.active = False
            self.players.clear()
            self.pool = 0
            return

        def get_players(self):
            return self.players

        def add_player(self, name: Player, bet: int):
            self.players.append([name, bet])

        def payout(self, name: Player, amount: int):
            name.add(amount)

    @commands.group(name="lottery",
                    aliases=[],
                    usage="<command>",
                    help="Start a lottery for big monies!", invoke_without_command=True)
    @commands.guild_only()
    async def lottery(self, ctx: commands.Context):
        print("pp")

    @lottery.command(name="start",
                     aliases=["s"],
                     usage="<bet> [seconds]",
                     help="Start a lottery with the desired amount of time. Only one lottery is available to be active!")
    @commands.guild_only()
    async def start(self, ctx: commands.Context, bet: int, duration: float = 60.0):
        print(self.active_lottery.active)
        if self.active_lottery.active == True:
            await ctx.send("There is already a lottery happening! Do $lottery join <bet>", reference=ctx.message)
        else:
            player = PlayerUtils.verify_player(ctx.author)
            if player.get_balance() < bet:
                await ctx.send("Insufficient Funds.", reference=ctx.message)
            else:
                self.active_lottery.active = True
                await ctx.send(f"You started a lottery. It will end in ~{duration} seconds", reference=ctx.message)
                self.active_lottery.add_player(player, bet)
                player.add(-bet)
                await self.active_lottery.start(float(duration))

    @lottery.command(name="join",
                     aliases=["j"],
                     usage="<bet>",
                     help="Join the lottery!")
    @commands.guild_only()
    async def join(self, ctx: commands.Context, bet: int):
        if self.active_lottery.active == False:
            await ctx.send("There is no current lottery! Do $lottery start <bet> [seconds] to start a lottery.", reference=ctx.message)
        else:
            player = PlayerUtils.verify_player(ctx.author)
            if player.get_balance() < bet:
                await ctx.send("Insufficient Funds.", reference=ctx.message)
            else:
                player.add(-bet)
                await ctx.send(f"You joined the lottery! Total in the pool: {self.active_lottery.pool}", reference=ctx.message)
                self.active_lottery.add_player(player, bet)


def setup(bot):
    bot.add_cog(Economy(bot))
