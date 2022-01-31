import discord
from discord.ext import commands
from discord.commands import slash_command, Option


class CargoBay(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    GUILD_ID = int(206125299639910402)

    @slash_command(guild_ids=[GUILD_ID])
    async def hi(self, ctx):
        await ctx.respond(f"Hello !")


def setup(bot: commands.Bot):
    bot.add_cog(CargoBay(bot))
