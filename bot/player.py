class Player:
    id: str
    name: str

    accounts: list

    def __init__(self, data):
        self.update(data)

    def update(self, data):
        self.id = data['id']
        self.name = data['name']
        self.accounts = data['accounts']


class Account:
    id: str
    balance: int

    def __init__(self, data):
        self.update(data)

    def update(self, data):
        self.id = data['id']
        self.balance = data['balance']
