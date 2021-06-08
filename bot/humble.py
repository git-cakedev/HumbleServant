import os
import discord
from discord.ext import commands, commands
from discord.ext.commands.cog import Cog


# change other's nickname for an hour
# bencoin reacts give sender a coin
# .imtrapped posts a pic of a trap

try:
    TOKEN = os.environ["DISCORD_TOKEN"]
    GUILD = os.environ["DISCORD_GUILD"]
except:
    print("DISCORD_TOKEN and/or DISCORD_GUILD environment variables not found!")
    raise discord.DiscordException


class Bot(commands.Cog):

    def __init__(self, command_prefix, self_bot):
        commands.Bot.__init__(
            self, command_prefix=command_prefix, self_bot=self_bot)

        self.added_commands()

    def added_commands(self):
        @self.event
        async def on_ready():
            # guilds = discord.utils.find(lambda g:  g.name == GUILD, bot.guilds)

            await bot.change_presence(status=discord.Status.online, activity=discord.Game("Listening to .help"))

            print(f'{bot.user.name} is connected\n')

        @self.event
        async def on_command_error(ctx, error):
            if isinstance(error, commands.errors.CheckFailure):
                await ctx.send('You do not have the correct role for this command.')

        @self.command(help="PONG!")
        async def ping(ctx):
            await ctx.send(f"🏓 Pong with {str(round(bot.latency, 2))}")

        @self.command(help="Who sent this message?")
        async def whoami(ctx):
            await ctx.send(f"You are {ctx.message.author.name}")

        @self.command(help="clears the last 2 messages. FOR TEST PURPOSES")
        async def clear(ctx, amount=3):
            await ctx.channel.purge(limit=amount)

        @self.command(help="adds two numbers separated by spaces")
        async def add(ctx, a: int, b: int):
            await ctx.send(a + b)

        @self.command()
        @commands.has_role("Archduke of Celibacy")
        async def init(ctx):
            data = {
                "id": ctx.message.author.id,
                "name": ctx.message.author.name + '#' + ctx.message.author.discriminator,
                "accounts": []
            }
            print(data)
            user = Player(data)
            print(user)
            user.add_account()
            print(user)


bot = Bot(command_prefix=".", self_bot=False)
bot.run(TOKEN)


class Player(commands.Cog):
    id: str
    name: str

    balance: int

    def __str__(self) -> str:
        return 'id= {} name= {} balance= {}'.format(self.id, self.name, self.balance)

    def __init__(self, bot) -> None:

        return self
        # def __init__(self, data):

        #     self.update(data)

        # def update(self, data):
        #     self.id = data['id']
        #     self.name = data['name']
        #     self.balance = data['balance']

    async def set_balance(self, amount):
        self.balance = amount
        await self.balance

    async def deposit(self, amount):
        await self.balance + amount

    async def withdraw(self, amount):
        if self.balance > amount:
            await self.balance - amount
        else:
            print(f"account balance too low! account: {self.name}")
            return ValueError
