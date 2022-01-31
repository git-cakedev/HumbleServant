import discord
from discord.ext import commands


class EventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                description=f"**<:error:897382665781669908> You are missing required arguments!\nMissing argument: `{error.param}`**", color=discord.Color.red())
            await ctx.send(embed=embed, delete_after=10, reference=ctx.message)
        elif isinstance(error, commands.errors.CommandNotFound):
            embed = discord.Embed(
                description=f"**<:error:897382665781669908> Couldn't find that command!**", color=discord.Color.red())
            await ctx.send(embed=embed, delete_after=10, reference=ctx.message)
        elif isinstance(error, commands.errors.BadArgument):
            embed = discord.Embed(
                description=f"**<:error:897382665781669908> Invalid datatype passed in.\nError: `{str(error)}`**", color=discord.Color.red())
            await ctx.send(embed=embed, reference=ctx.message)
        elif isinstance(error, commands.errors.BotMissingPermissions):
            embed = discord.Embed(
                description=f"**<:error:897382665781669908> I am missing required permissions!**", color=discord.Color.red())
            await ctx.send(embed=embed, reference=ctx.message)
        elif isinstance(error, commands.errors.MemberNotFound):
            embed = discord.Embed(
                description=f"**<:error:897382665781669908> I can't find that user!**", color=discord.Color.red())
            await ctx.send(embed=embed, delete_after=10)
        elif isinstance(error, commands.errors.NotOwner):
            embed = discord.Embed(
                description=f"**<:error:897382665781669908> This command is a `owner` only command.**", color=discord.Color.red())
            await ctx.send(embed=embed, delete_after=10, reference=ctx.message)
        elif isinstance(error, commands.errors.TooManyArguments):
            embed = discord.Embed(
                description=f"**<:error:897382665781669908> Too many arguments {ctx.author.mention}!**", color=discord.Color.red())
            await ctx.send(embed=embed, delete_after=10, reference=ctx.message)
        elif isinstance(error, commands.MissingPermissions):
            permissions = "\n".join(error.missing_permissions)
            embed = discord.Embed(
                description=f"**<:error:897382665781669908> You are missing reqired permission(s)!\n{permissions}**", color=discord.Color.red())
            await ctx.send(embed=embed, delete_after=10, reference=ctx.message)
        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                description=f"**<:error:897382665781669908> Keep cool!\nThe **{ctx.command.name}** command is on a cooldown. Wait for `{error.retry_after:.1f}`s**", color=discord.Color.red())
            await ctx.send(embed=embed, reference=ctx.message)
        elif isinstance(error, commands.DisabledCommand):
            embed = discord.Embed(
                description="<:error:897382665781669908> This command is disabled :(", color=discord.Color.red())
            await ctx.send(embed=embed, reference=ctx.message)
        else:
            raise error
    """
    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed = discord.Embed(
                description="**<:error:897382665781669908> You are missing required arguments!**", color=discord.Color.red())
            await ctx.respond(embed=embed)
        elif isinstance(error, commands.errors.CommandNotFound):
            embed = discord.Embed(
                description=f"**<:error:897382665781669908> Couldn't find a command named {ctx.command}!**", color=discord.Color.red())
            await ctx.respond(embed=embed)
        elif isinstance(error, commands.errors.BadArgument):
            embed = discord.Embed(
                description=f"**<:error:897382665781669908> Invalid datatype passed in.\nError: `{str(error)}`**", color=discord.Color.red())
            await ctx.respond(embed=embed)
        elif isinstance(error, commands.errors.BotMissingPermissions):
            embed = discord.Embed(
                description=f"**<:error:897382665781669908> I am missing required permissions!**", color=discord.Color.red())
            await ctx.respond(embed=embed)
        elif isinstance(error, commands.errors.MemberNotFound):
            embed = discord.Embed(
                description=f"**<:error:897382665781669908> I can't find that user!**", color=discord.Color.red())
            await ctx.respond(embed=embed)
        elif isinstance(error, commands.errors.NotOwner):
            embed = discord.Embed(
                description=f"**<:error:897382665781669908> This command is a `owner` only command.**", color=discord.Color.red())
            await ctx.respond(embed=embed)
        elif isinstance(error, commands.errors.TooManyArguments):
            embed = discord.Embed(
                description=f"**<:error:897382665781669908> Too many arguments {ctx.author.mention}!**", color=discord.Color.red())
            await ctx.respond(embed=embed)
        elif isinstance(error, commands.errors.MissingPermissions):
            embed = discord.Embed(
                description=f"**<:error:897382665781669908> You are missing reqired permission(s)!**", color=discord.Color.red())
            await ctx.respond(embed=embed)
        else:
            raise error
        """


def setup(bot):
    bot.add_cog(EventsCog(bot))
