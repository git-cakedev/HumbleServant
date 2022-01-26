import discord
from discord.ext import commands
from Cogs.stock import StockUtils
from Cogs.player import PlayerUtils


class StockExchange(commands.Cog, name="StockExchange"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def stonk(self, ctx: commands.Context):
        await ctx.send("template command")

    @stonk.command(name="find",
                   usage="<symbol>",
                   help="Enter a Ticker symbol to show information about the stock.")
    async def find(self, ctx: commands.Context, symbol: str):

        price = StockUtils.get(symbol)
        if price == None:
            await ctx.send("My advanced AI was unable to find that symbol.", reference=ctx.message)
        else:
            bencoin_price = StockUtils.convert(price)
            await ctx.send("{} current price: ${}USD or {} bencoins".format(symbol, price, bencoin_price), reference=ctx.message)

    @stonk.command(name="buy",
                   usage="<symbol> <shares>",
                   help="Buy shares of given stonk at market price")
    async def buy(self, ctx: commands.Context, symbol: str, shares: int):
        player = PlayerUtils.verify_player(ctx.author)

    @commands.group(name="stake",
                    help="Stake into the pool to earn interest over time.",
                    invoke_without_command=True)
    async def stake(self, ctx: commands.Context):
        player = PlayerUtils.verify_player(ctx.author)

        if not 'bencoin' in player.get_stocks().keys():
            await ctx.send("Make a deposit to start earning!", reference=ctx.message)
        else:
            current_price = StockUtils.convert(StockUtils.get("ETH-USD"))
            stock = player.get_stocks()['bencoin']
            last_price = stock["price"]
            delta_price = (current_price - last_price)/last_price

            percent_change = delta_price * 100
            amount = round((1+delta_price) * stock["amount"])
            await ctx.send("Your earnings: {}\nPercent Change: {}%".format(amount, round(percent_change, 2)), reference=ctx.message)

    @stake.command(name="deposit",
                   usage="<amount>",
                   aliases=['d'],
                   help="Stake into the pool to earn interest over time.")
    async def deposit(self, ctx: commands.Context, amount: int):
        player = PlayerUtils.verify_player(ctx.author)
        if (amount < 1) or (player.get_balance() < amount):
            await ctx.send("Insufficient Funds.", reference=ctx.message)
        else:
            if 'bencoin' in player.get_stocks().keys():
                await ctx.send("You must withdraw staked bencoin first!", reference=ctx.message)
            else:
                player.add(-amount)
                bencoin_price = StockUtils.convert(StockUtils.get("ETH-USD"))
                player.get_stocks()['bencoin'] = {
                    "amount": amount, "price": bencoin_price}

                await ctx.send("You staked {} bencoins.".format(amount), reference=ctx.message)

    @stake.command(name="withdraw",
                   aliases=['w'],
                   help="Withdraw your stake.")
    async def withdraw(self, ctx: commands.Context):
        player = PlayerUtils.verify_player(ctx.author)
        if not 'bencoin' in player.get_stocks().keys():
            await ctx.send("You have no staked bencoins.", reference=ctx.message)
        else:
            stake = player.pop_stock('bencoin')

            amount = stake['amount']
            last_price = stake['price']
            price = StockUtils.get("ETH-USD")
            current_price = StockUtils.convert(price)
            delta_price = (current_price - last_price)/last_price

            owed = round((1+delta_price) * amount)

            player.add(owed)

            await ctx.send("You withdrew {} bencoins. The Exchange thanks you.".format(owed), reference=ctx.message)


def setup(bot):
    bot.add_cog(StockExchange(bot))


class Stake(dict):
    def __init__(self, price: int, amount: int):
        self.price = price
        self.amount = amount
