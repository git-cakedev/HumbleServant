import discord
from discord.ext import commands
from discord.commands import slash_command, Option


class CargoBay(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    GUILD_ID = int(206125299639910402)
    '''
    @slash_command(guild_ids=[GUILD_ID])
    async def cargo(self, ctx: discord.Member):
        await ctx.respond(f"Hello !")
    '''
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        voice_channels = self.bot.get_guild(self.GUILD_ID).voice_channels

        if (before.channel == None) and (after.channel in voice_channels):
            print("User joined a vchannel")
        #print("before" + str(before.channel))
        #print("after" + str(after.channel))
        # if after.channel.id in self.vchannels and not member.bot:
        #    print("User joined a vchannel")


def setup(bot: commands.Bot):
    bot.add_cog(CargoBay(bot))


class Item(dict):
    commons = [
        'Blaster Rifle',
        'Spice Dime Bag',
        'Lethverse Pilsner',
        'Holocards',
        'Alienboy Magazine',
        'Vibroknife',
        'Stolen Datapad',
        'Broken Jetpack',
        'Grenades',
        'Bounty Contract',
        'Smuggled Anime'
    ]

    rares = [
        'Mimi Poster',
        'Portable Holodancer',
        'Speeder Bike',
        'Alien Juiced Wine',
        'Case of Lethversian Pilsner',
        'Token of Kingpin\'s Love',
        'Alien Anime Body Pillow',
        'Spice Purveyor\'s Handbook'
    ]

    legendarys = [
        'Noah\'s Left Nut',
        'Vintage Dexeo Mixtape',
        'Vania Bandana',
        'Vintage Old World Soviet Beret',
        'Mimi\'s Personal Diary',
        'Communist Manifesto',
        'Liver\'s Personal Holodancer Collection'
    ]
