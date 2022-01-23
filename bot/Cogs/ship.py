class Ship():
    # data = {
    #    "name": str,
    #    "hp": int,
    #    "speed": int,
    #    "sp": int,
    #    "weapons": []
    # }

    def __init__(self, name="Ship 1", hp=100, speed=1, sp=0, weapons=[], value=100):
        self.data = {}
        self.data["name"] = name
        self.data["hp"] = hp
        self.data["speed"] = speed
        self.data["sp"] = sp
        self.data["weapons"] = weapons
        self.data["value"] = value

    def __str__(self):
        result = "Name: {}\n\t HP: {}\n\t Speed: {}\n\t Shield Power: {}\n\t Weapons: {}\n\t Value: {} bencoins".format(
            self.data["name"], self.data["hp"], self.data["speed"], self.data["sp"], self.data["weapons"], self.data["value"])
        return result

    def get_data(self) -> dict:
        return self.data
