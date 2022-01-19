import discord
from discord.ext import commands


class ping(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        
    @commands.command() # this is for making a command
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}')
    

def setup(bot:commands.Bot):
    bot.add_cog(ping(bot))