import json
import discord
from discord.ext import commands

with open("player_data.json", "r") as data_file:
    data = json.load()


class Player(commands.Cog):
    id: str
    name: str

    balance: int

    def __init__(self, bot: commands.Bot, data):
        self.bot = bot
        self.id = data['id']
        self.name = data['name']
        self.balance = data['balance']

    def __str__(self) -> str:
        return 'id= {} name= {} balance= {}'.format(self.id, self.name, self.balance)

    def set_balance(self, amount):
        self.balance = amount
        return self.balance

    def add(self, amount):
        return self.balance + amount

    @commands.command(name="commandName",
                      usage="<usage>",
                      description="description")
    @commands.guild_only()
    @commands.has_permissions()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def commandName(self, ctx: commands.Context):
        await ctx.send("template command")


def setup(bot: commands.Bot):
    bot.add_cog(Player(bot))
