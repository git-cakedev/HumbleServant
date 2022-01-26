import discord
from discord.ext import commands
from Cogs.player import PlayerUtils
import Cogs.ship as Ship
import math


class Battleship(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def ship(self, ctx: commands.Context):
        await ctx.send("Do \"$help ship\" to see ship commands.")
        await self.list(ctx)

    @ship.command(name="buy",
                  usage="<name>",
                  help="Buy a basic ship for 100 bencoins")
    async def buy(self, ctx, name="Ship"):
        player = PlayerUtils.verify_player(ctx.author)
        if player["balance"] < 100:
            await ctx.send("Insufficient funds.")
            return

        ship = Ship.Ship(name=name)

        if not "ships" in player.keys():
            player["ships"] = []
        for s in player["ships"]:
            if s["name"] == name:
                await ctx.send("You already have a ship with that name in your dock!")
                return

        player["ships"].append(ship.get_data())

        await ctx.send("Congragulations, the mechanics are preparing your new ship!")

    @ship.command(name="list",
                  aliases=["l"],
                  help="Shows a list of currently owned ships.")
    async def list(self, ctx):
        player = PlayerUtils.verify_player(ctx.author)
        ships = player.setdefault("ships", {})
        message = "Current ships in dock:"
        for ship in ships:
            s = Ship.Ship(name=ship["name"], hp=ship["hp"],
                          speed=ship["speed"], sp=ship["sp"], modules=ship["modules"], weapons=ship["weapons"], value=ship["value"])
            data = str(s)

            message = message + "\n" + "\n" + str(s)

        await ctx.send(message)

    @ship.command(name="sell",
                  usage="\"<name>\"",
                  help="Sells given ship to the shop. Note: You will receive 80% of the ship's value.")
    async def sell(self, ctx, name: str):
        player = PlayerUtils.verify_player(ctx.author)
        # print(player["ships"])

        for ship in player["ships"]:
            if ship["name"] == name:
                value = ship["value"] * 0.8
                value = math.floor(value)
                player["balance"] += value
                player["ships"].pop(player["ships"].index(ship))
                await ctx.send("Nice doing business with you! {} bencoins were sent to your wallet.".format(value))
                self.save_json()
                return
        await ctx.send("I don't see a ship with that name in your dock...")

    @ship.group(invoke_without_command=True)
    async def miner(self, ctx):
        await ctx.send("Do \"$help miner\" to see miner commands.")
    '''
    @miner.command(name="buy",
                   usage="<ship_name>",
                   help="Buys a bencoin miner for the given ship for 1000 bencoins")
    async def buy(self, ctx, ship_name: str):
        player = self.get_player(ctx.author)

        if not "ships" in player.keys():
            player["ships"] = []

        for ship in player["ships"]:
            if ship["name"] == ship_name:
                s = Ship.Ship(name=ship["name"], hp=ship["hp"],
                              speed=ship["speed"], sp=ship["sp"], modules=ship["modules"], weapons=ship["weapons"], value=ship["value"])

                data = s.get_data()
                if data["modules"].count("miner") > 0:
                    await ctx.send("This ship already has a miner installed!")
                    return
                else:
                    s.add_module("miner")
                    await ctx.send("You have installed a bencoin miner to {}".format(ship_name))
    '''


def setup(bot: commands.Bot):
    bot.add_cog(Battleship(bot))
