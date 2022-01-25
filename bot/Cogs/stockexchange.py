import discord
from discord.ext import commands
from Cogs.stock import Stock
from Cogs.stock import StockUtils


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
            await ctx.send("My advanced AI was not able to find that symbol.")
        else:
            bencoin_price = StockUtils.convert(price)
            await ctx.send("{} current price: ${}USD or {} bencoins".format(symbol, price, bencoin_price), reference=ctx.message)


def setup(bot):
    bot.add_cog(StockExchange(bot))
