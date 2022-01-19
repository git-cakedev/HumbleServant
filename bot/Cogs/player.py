class Player():
    data = {
        'name': "",
        'balance': 0
    }

    def __str__(self) -> str:
        return 'name: {} balance: {}'.format(self.get_name(), self.get_balance())

    def __json__(self):
        return self.data

    def set_balance(self, amount):
        self.data['balance'] = amount
        return self.data['balance']

    def get_balance(self):
        return self.data['balance']

    def get_data(self):
        return self.data

    def add(self, amount):
        return self.data['balance'] + amount

    def get_name(self):
        return self.data['id']

    def set_name(self, name):
        self.data['name'] = name
        return self.data['name']
