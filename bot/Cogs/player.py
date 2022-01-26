import discord
import json


class Player():

    def __init__(self, name="", balance=1000, ships={}, items={}, stocks={}) -> None:
        self.data = {}
        self.data["name"] = name
        self.data["balance"] = balance
        self.data["ships"] = ships
        self.data["items"] = items
        self.data["stocks"] = stocks

    def __str__(self) -> str:
        return 'name: {} balance: {}'.format(self.get_name(), self.get_balance())

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def set_balance(self, amount: int) -> int:
        self.data['balance'] = amount
        return self.set_balance()

    def get_balance(self) -> int:
        return self.data['balance']

    def add(self, amount: int) -> int:
        self.data['balance'] += amount
        return self.get_balance()

    def get_data(self) -> dict:
        return self.data

    def get_name(self) -> str:
        return self.data['name']

    def set_name(self, name: str) -> str:
        self.data['name'] = name
        return self.data['name']

    def get_stocks(self) -> dict:
        return self.data['stocks']

    def add_stock(self, name: str, data: dict) -> dict:
        self.data['stocks'][name] = data
        return self.data['stocks'][name]

    def pop_stock(self, name: str) -> dict:
        if name in self.data['stocks'].keys():
            return self.data['stocks'].pop(name)
        else:
            return None


class PlayerUtils():
    players = {}

    def verify_player(player: discord.Member or discord.User) -> Player:
        id = str(player.id)
        if not id in PlayerUtils.players.keys():
            return PlayerUtils.register_player(player)
        else:
            p = PlayerUtils.players[id]
            return p

    def register_player(player: discord.Member or discord.User) -> Player:
        full_name = player.name + "#" + str(player.discriminator)
        p = Player(name=full_name, stocks={})
        PlayerUtils.players[str(player.id)] = p
        return p

    def load_player_json():
        with open('data.json', "r") as file:
            data = json.load(file)

            for item in data.keys():
                p = Player(name=data[item]["name"],
                           balance=data[item]["balance"],
                           stocks=data[item]["stocks"])
                PlayerUtils.players[item] = p

    def save_player_json():
        with open('data.json', "w") as file:
            dumpd = {}
            for id in PlayerUtils.players.keys():
                dumpd[id] = PlayerUtils.players.get(id).get_data()

            json.dump(dumpd, file, indent=4)

    def get_playerdict(self) -> dict:
        return self.players
