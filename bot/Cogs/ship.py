class Ship():
    data = {
        "name": str,
        "hp": int,
        "speed": int,
        "sp": int,
        "weapons": []
    }

    def __init__(self, name="Ship 1", hp=100, speed=1, sp=0, weapons=[]):
        self.data.name = name
        self.data.hp = hp
        self.data.speed = speed
        self.data.sp = sp
        self.data.weapons = weapons

    def get_data(self) -> dict:
        return self.data
