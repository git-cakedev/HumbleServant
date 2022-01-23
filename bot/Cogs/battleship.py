import discord
from discord.ext import commands
import json
import Cogs.ship as Ship
import math


class Battleship(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def save_json(self):
        with open('data.json', "w") as file:
            new_data = self.bot.players
            json.dump(new_data, file, indent=4)

    def get_player(self, player: discord.Member or discord.User):
        id = str(player.id)
        result = self.bot.players.setdefault(
            id, {"name": player.name + "#" + str(player.discriminator), "balance": 10, "blacklisted": True})
        return result

    @commands.group(invoke_without_command=True)
    async def ship(self, ctx: commands.Context):

        await ctx.send("Do \"$help ship\" to see ship commands.")
        await self.list(ctx)

    @ship.command(name="buy",
                  aliases=["b"],
                  usage="[optional: <name>]",
                  help="Buy a basic ship for 100 bencoins")
    async def buy(self, ctx, type="generic", name="Ship"):
        player = self.get_player(ctx.author)
        if player["balance"] < 0:
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
        self.save_json()
        await ctx.send("Congragulations, the mechanics are preparing your new ship!")

    @ship.command(name="list",
                  aliases=["l"],
                  help="Shows a list of currently owned ships.")
    async def list(self, ctx):
        player = self.get_player(ctx.author)
        ships = player.setdefault("ships", {})
        message = "Current ships in dock:"
        for ship in ships:
            s = Ship.Ship(name=ship["name"], hp=ship["hp"],
                          speed=ship["speed"], sp=ship["sp"], weapons=ship["weapons"], value=ship["value"])
            data = str(s)

            message = message + "\n" + "\n" + str(s)

        await ctx.send(message)

    @ship.command(name="sell",
                  aliases=["s"],
                  usage="\"<name>\"",
                  help="Sells given ship to the shop. Note: You will receive 80% of the ship's value.")
    async def sell(self, ctx, name: str):
        player = self.get_player(ctx.author)
        # print(player["ships"])

        for ship in player["ships"]:
            if ship["name"] == name:
                value = ship["value"] * 0.8
                value = math.floor(value)
                player["balance"] += value
                player["ships"].pop(player["ships"].index(ship))
                await ctx.send("Nice doing business with you! {} bencoins were sent to your wallet.".format(value))
                return
        await ctx.send("I don't see a ship with that name in your dock...")


def setup(bot: commands.Bot):
    bot.add_cog(Battleship(bot))
