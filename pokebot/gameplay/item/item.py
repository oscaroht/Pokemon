import os
from sqlalchemy import create_engine
from ...fundamentals import config

def load_items():
    # loads all items from database
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    engine = create_engine(f"postgresql+psycopg2://postgres:{config('../../../users.ini', 'postgres', 'password')}@localhost/pokemon")

    with engine.connect() as con:
        for row in con.execute(f"select * from vault.all_items;"):
            Item(row['item_id'], row['item_name'], row['buy'], row['sell'], 0)
        for row in con.execute(f"select * from vault.tmhm;"):
            Item(row['item_id'], row['move_code'], row['price'], None, 0)
        for row in con.execute(f"select * from vault.badges;"):
            Item(row['item_id'], row['badge_name'], None, None, 0)
        for row in con.execute(f"select * from vault.own_items;"):
            Items.get_item_by_id(row['item_id']).amount = row['amount']

class IterItems(type):
    def __iter__(cls):
        return iter(cls.all['name'].values())

class Items(metaclass=IterItems):

    all = {'id':{}, 'name':{}}

    @classmethod
    def get_item_by_id(cls, id):
        return cls.all['id'][id]

    @classmethod
    def get_item_by_name(cls, name):
        if name in cls.all['name']:
            return cls.all['name'][name]
        return None

    @classmethod
    def find_item_by_name(cls, name):
        import difflib
        correct_name = difflib.get_close_matches(name, [str(x) for x in list(cls.all['name'].keys())], n=1)[0]
        return cls.all['name'][correct_name]

    @classmethod
    def get_item_price_by_name(cls, name):
        item = cls.get_item_by_name(name)
        return item.buy

    @classmethod
    def do_i_have(cls, item_name):
        if item_name in cls.all['name']:  # default look through keys
            item = cls.get_item_by_name(item_name)
            if item is not None and item.amount > 0:
                return True
        return False

    @classmethod
    def new_game(cls):
        for item in cls.all['name'].values():
            item.amount = 0

class Item:

    def __init__(self, item_id, item_name, buy, sell, amount, add_to_all=True):
        self.id = item_id
        self.name = item_name
        self.buy = buy
        self.sell = sell
        self.amount = amount

        if add_to_all:
            Items.all['id'][self.id] = self
            Items.all['name'][self.name] = self

    def __str__(self):
        return f"Item: {self.name}, amount {self.amount}"

    def lower_amount(self, subtract=1):
        if self.amount - subtract >= 0:
            self.amount -= subtract
            return
        raise Exception(f"Unable to lower amount for amount {self.amount}")

    def add_amount(self, added=1):
        if added > 0 and added < 99:
            self.amount += added
            return
        raise Exception(f"Unable to add {added} to {self}")



load_items()

if __name__ == "__main__":
    test=1