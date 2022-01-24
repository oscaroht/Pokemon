import os
from sqlalchemy import create_engine
from fundamentals.config import config

def load_items():
    # loads all items from database
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    engine = create_engine(f"postgresql+psycopg2://postgres:{config('../users.ini','postgres','password')}@localhost/pokemon")

    with engine.connect() as con:
        for row in con.execute(f"select * from vault.all_items;"):
            Item(row['item_id'], row['item_name'], row['buy'], row['sell'])
        for row in con.execute(f"select * from vault.tmhm;"):
            Item(row['item_id'], row['move_code'], row['price'], None)

def load_own_items():
    # loads own items from database
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    engine = create_engine(f"postgresql+psycopg2://postgres:{config('../users.ini','postgres','password')}@localhost/pokemon")

    query = "select item_id, a.item_name, a.buy, a.sell, amount  from vault.all_items a join vault.own_items using(item_id);"
    with engine.connect() as con:
        for row in con.execute(query):
            OwnItems(row['item_id'], row['item_name'], row['buy'], row['sell'], row['amount'])

class Gamestats:

    items = []

    money = 0



class Item:

    all = {'id':{}, 'name':{}}

    def __init__(self, item_id, item_name, buy, sell, add_to_all=True):
        self.item_id = item_id
        self.item_name = item_name
        self.buy = buy
        self.sell = sell

        if add_to_all:
            Item.all['id'][self.item_id] = self
            Item.all['name'][self.item_name] = self

    @classmethod
    def get_item_by_id(cls, id):
        return cls.all['id'][id]

    @classmethod
    def get_item_by_name(cls, name):
        if name in cls.all['name']:
            return cls.all['name'][name]
        return None

    @classmethod
    def get_item_price_by_name(cls, name):
        item = cls.get_item_by_name(name)
        return item.buy

class OwnItems(Item):

    all = {'id':{}, 'name':{}}  # example all['name']['Poke Ball'] = pokeball_object   {'poke ball': object}

    def __init__(self, item_id, item_name, buy, sell, amount):
        super(OwnItems,self).__init__(item_id, item_name, buy, sell, add_to_all=False)
        self.amount = amount
        OwnItems.all['id'][self.item_id] = self
        OwnItems.all['name'][self.item_name] = self

    def lower_amount(self, amount=1):
        if self.amount > 0:
            self.amount -= amount
            return
        raise Exception(f"Unable to lower amount for amount {self.amount}")

    # def increase_amount(self, amount):
    #     if self.amount > 0:
    #         self.amount -= amount
    #         return
    #     raise Exception(f"Unable to increase amount for amount {self.amount}")

    @classmethod
    def add_item_by_name(cls, item_name, added_amount):
        if item_name in cls.all['name']:
            own_item_obj = cls.all['name'][item_name]
            own_item_obj.amount += added_amount
        else:
            # add object to all
            item_obj = Item.get_item_by_name(item_name)
            OwnItems(item_obj.item_id, item_obj.item_name, item_obj.buy, item_obj.sell, added_amount)

    # @classmethod
    # def get_item_by_id(cls, id):
    #     return cls.all['id'][id]
    #
    # @classmethod
    # def get_item_by_name(cls, name):
    #     if name in cls.all['name']:
    #         return cls.all['name'][name]
    #     return None

    @classmethod
    def do_i_have(cls, item_name):
        if item_name in cls.all['name']:  # default look through keys
            item = cls.get_item_by_name(item_name)
            if item is not None and item.amount > 0:
                return True
        return False

    @classmethod
    def new_game(cls):
        cls.all = {'id':{}, 'name':{}}


load_items()
load_own_items()
if __name__ == "__main__":
    test=1