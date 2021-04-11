
from sqlalchemy import create_engine
from fundamentals.config import config
import os
import pandas as pd

class PP_below_zero(Exception):
    pass

class PartyError(Exception):
    pass

def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

def load_pokemon():
    query = """select 
    a.own_pokemon_id,
    a.pokemon_id,
    a.own_pokemon_name,
    b.type1,
    b.type2,
    a.lvl,
    a.status,
    a.hp,
    a.max_hp,
    a.atk,
    a.defe ,
    a.spa ,
    a.spd,
    a.spe ,
    a.move1_pp ,
    a.move2_pp ,
    a.move3_pp, 
    a.move4_pp , 
    c.move_id as move1_id,
    d.move_id as move2_id,
    e.move_id as move3_id,
    f.move_id as move4_id,
    c.move_name as move1,
    d.move_name as move2,
    e.move_name as move3,
    f.move_name as move4,
    c.move_type as move1_type,
    d.move_type as move2_type,
    e.move_type as move3_type,
    f.move_type as move4_type,
    c.move_power as move1_power,
    d.move_power as move2_power,
    e.move_power as move3_power,
    f.move_power as move4_power,
    c.move_accuracy as move1_accuracy,
    d.move_accuracy as move2_accuracy,
    e.move_accuracy as move3_accuracy,
    f.move_accuracy as move4_accuracy,
    c.max_pp as max_pp1,
    d.max_pp as max_pp2,
    e.max_pp as max_pp3,
    f.max_pp as max_pp4
    from mart.own_pokemon a
    join mappings.pokemon b on a.pokemon_id = b.pokemon_id 
    join mappings.pokemon_move c on a.move1_id = c.move_id 
    join mappings.pokemon_move d on a.move2_id = d.move_id 
    join mappings.pokemon_move e on a.move3_id = e.move_id 
    join mappings.pokemon_move f on a.move4_id = f.move_id; """

    if 'pokemon_table' not in globals() or 'pokemon_move_table' not in globals() or 'own_pokemon' not in globals() or 'party' not in globals():
        global df_pokemon
        global df_moves
        global own_pokemon
        global party

        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        engine = create_engine(f"postgresql+psycopg2://postgres:{config('../users.ini','postgres','password')}@localhost/pokemon")

        with engine.connect() as con:
            df_pokemon = pd.read_sql_table('pokemon', con=con, schema='mappings', index_col='pokemon_id')
            df_moves = pd.read_sql_table('pokemon_move', con=con, schema='mappings', index_col='move_id')
            df_party = pd.read_sql_table('party', con=con, schema='mart')
            #df_own_pokemon = pd.read_sql_table('own_pokemon', con=con, schema='mart')
            df_own_pokemon = pd.read_sql(query,con=con)

        own_pokemon = AllOwnPokemon()
        for index, row in df_own_pokemon.iterrows():
            move1 = OwnMove(row['move1_id'], row['move1'], row['move1_type'], row['move1_power'], row['move1_accuracy'],
                            row['max_pp1'], row['move1_pp'])

            stats = {'hp': row['max_hp'], 'atk': row['atk'], 'def': row['defe'], 'spa': row['spa'], 'spd': row['spd'],
                     'spe': row['spe']}

            own_pokemon.append(OwnPokemon(row['pokemon_id'], row['own_pokemon_name'], row['type1'], row['type2'], stats,
                                          row['own_pokemon_id'], row['own_pokemon_name'], row['lvl'], move1,
                                          current_hp=row['hp'], status=row['status']))
        party = Party()  # create empty party
        for index, row in df_own_pokemon.iterrows():
            own_id = row['own_pokemon_id']
            party.add(own_pokemon.get_pokemon_by_id(own_id))


class Move:
    def __init__(self, id,name, type1, power, accuracy, max_pp):
        self.id = id
        self.name = name
        self.type = type1
        self.power = power
        self.accuracy = accuracy
        self.max_pp = max_pp

class OwnMove(Move):
    def __init__(self, id, name, type1, power, accuracy, max_pp, pp):
        super(OwnMove,self).__init__(id, name, type1, power, accuracy, max_pp)
        self.pp = pp

    def lower_pp(self):
        if self.pp > 0:
            self.pp -=1
        else:
            raise PP_below_zero()


class Pokemon:

    def __init__(self,pokemon_id, pokemon_name, type1, type2, stats):#, base_stats):
        self.pokemon_id = pokemon_id
        self.name = pokemon_name
        self.type1 = type1
        self.type2 = type2
        self.base_stats = stats # dict {'hp':82, 'atk':50, ...}
        #self.evolve = evolve # dict {'method':'level', 'by': 16, 'into_name': 'Charizard'}

class OwnPokemon(Pokemon):

    def __init__(self,pokemon_id, pokemon_name, type1, type2, stats, own_id,own_name,lvl, own_moves, current_hp = 0, status = 'normal'): # add some kind of move id or move object
        super(OwnPokemon, self).__init__(pokemon_id, pokemon_name, type1, type2, stats)

        self.own_id = own_id
        self.own_name =own_name
        # if you dont know (after caught) set stats to base_stats * level function and current_hp = 0
        self.stats = stats
        self.current_hp = current_hp
        self.status = status
        self.lvl = lvl

        self.move1 = own_moves
        self.move2 = own_moves
        self.move3 = own_moves
        self.move4 = own_moves

    def heal(self):
        self.move1.pp =self.move1.max_pp
        self.move2.pp = self.move2.max_pp
        self.move3.pp = self.move3.max_pp
        self.move4.pp = self.move4.max_pp
        self.current_hp = self.stats['max_hp']

    def lvl_up(self, new_lvl,hp, atk, defe, spa, spe):
        self.lvl +=1
        # update stats
        self.stats = {'hp':hp, 'atk':atk, 'def':defe, 'spa':spa, 'spd':spa, 'spe':spe }

    def save(self):
        query =f"""insert into mart.own_pokemon values ({self.own_id}, {self.pokemon_id},'{self.own_name}',{self.lvl},'{self.status}',{self.current_hp},{self.stats['hp']},{self.stats['atk']},{self.stats['def']},{self.stats['spa']},{self.stats['spd']},{self.stats['spe']},{self.move1.id},{self.move2.id},{self.move3.id}, {self.move4.id}, {self.move1.max_pp}, {self.move2.max_pp}, {self.move3.max_pp}, {self.move4.max_pp})
        on conflict (own_pokemon_id) do update set
        pokemon_id = excluded.pokemon_id,
        own_pokemon_name = excluded.own_pokemon_name,
        lvl = excluded.lvl,
        status = excluded.status,
        hp = excluded.hp,
        max_hp = excluded.max_hp,
        atk = excluded.atk,
        defe = excluded.defe,
        spa = excluded. spa,
        spd = excluded.spd,
        move1_id = excluded.move1_id, 
        move2_id = excluded.move2_id, 
        move3_id = excluded.move3_id, 
        move4_id = excluded.move4_id, 
        move1_pp = excluded.move1_pp,
        move2_pp = excluded.move2_pp,
        move3_pp = excluded.move3_pp,
        move4_pp = excluded.move4_pp
        ;"""

        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        engine = create_engine(f"postgresql+psycopg2://postgres:{config('../users.ini','postgres','password')}@localhost/pokemon")

        with engine.connect() as con:
            con.execute(query)

@singleton
class AllOwnPokemon(list):

    def get_pokemon_by_id(self,own_id):
        for i in range(len(self)):
            if self[i].own_id == own_id:
                return self[i]

@singleton
class Party(list):

    def add(self, pokemon):
        if len(self) < 6:
            self.append(pokemon)
        else:
            raise PartyError('Already 6 pokemon in party.')

    def rmv(self, pokemon): # remove is a list function
        if len(self.party) > 1:
            if pokemon in self:
                item = self.index(pokemon)
                self.pop(item)
            else:
                raise PartyError('Pokemon not found in party.')
        else:
            raise PartyError('Not enough pokemon in party to remove one.')

    def switch_position(self, pokemon, position = 0):
        if pokemon in self:
            old_position = self.index(pokemon)
            self.insert(position,self.pop(old_position))
        else:
            raise PartyError('Pokemon not found in party.')

    def heal(self):
        for pokemon in range(self):
            pokemon.heal()

    def save(self):
        query = "begin; truncate table mart.party;"
        for i in range(len(self)):
            query += f"insert into mart.party (own_pokemon_id) values ({self[i].own_id});"
        query += 'commit;'

        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        engine = create_engine(f"postgresql+psycopg2://postgres:{config('../users.ini','postgres','password')}@localhost/pokemon")
        with engine.connect() as con:
            con.execute(query)

if __name__=='__main__':
    load_pokemon()

    test=1

