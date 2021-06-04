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

    def add_account(self, account):
        self.accounts.append(account)
        return self.accounts


class Account:
    id: str
    balance: int

    def __init__(self, data):
        self.update(data)

    def update(self, data):
        self.id = data['id']
        self.balance = data['balance']

    def set_balance(self, amount):
        self.balance = amount
        return self.balance

    def add(self, amount):
        return self.balance + amount
