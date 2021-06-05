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

    def set_balance(self, amount):
        self.balance = amount
        return self.balance

    def add(self, amount):
        return self.balance + amount
