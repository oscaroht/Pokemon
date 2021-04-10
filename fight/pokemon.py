
from sqlalchemy import create_engine
from fundamentals.config import config
import os
import pandas as pd

class PP_below_zero(Exception):
    pass


def load_pokemon():

    query = """select 
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

    if 'pokemon_table' not in globals() or 'pokemon_move_table' not in globals() or 'own_pokemon_table' not in globals():
        global df_pokemon
        global df_moves
        global df_own_pokemon

        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        engine = create_engine(f"postgresql+psycopg2://postgres:{config('../users.ini','postgres','password')}@localhost/pokemon")

        with engine.connect() as con:
            df_pokemon = pd.read_sql_table('pokemon', con=con, schema='mappings', index_col='pokemon_id')
            df_moves = pd.read_sql_table('pokemon_move', con=con, schema='mappings', index_col='move_id')
            #df_own_pokemon = pd.read_sql_table('own_pokemon', con=con, schema='mart')

            df_own_pokemon = pd.read_sql(query,con=con)

class Move:
    def __init__(self, name, type1, power, accuracy, max_pp):
        self.id = id
        self.name = name
        self.type = type1
        self.power = power
        self.accuracy = accuracy
        self.max_pp = max_pp

class OwnMove(Move):
    def __init__(self, name, type1, power, accuracy, max_pp, pp):
        super(OwnMove,self).__init__(name, type1, power, accuracy, max_pp)
        self.pp = pp

    def lower_pp(self):
        if self.pp > 0:
            self.lower_pp()
        else:
            raise PP_below_zero()


class Pokemon:

    def __init__(self, name, type1, type2):#, base_stats):
        self.name = name
        self.type1 = type1
        self.type2 = type2
        #self.base_stats = base_stats # dict {'hp':82, 'atk':50, ...}
        #self.evolve = evolve # dict {'method':'level', 'by': 16, 'into_name': 'Charizard'}




class OwnPokemon(Pokemon):

    def __init__(self, name, type1, type2, stats, move, current_hp = 0, status = 'normal'): # add some kind of move id or move object
        super(OwnPokemon, self).__init__(name, type1, type2)

        # if you dont know (after caught) set stats to base_stats * level function and current_hp = 0
        self.stats = stats
        self.current_hp = current_hp
        self.status = status

        self.move = move



if __name__=='__main__':
    load_pokemon()

    party=[]
    for index, row in df_own_pokemon.iterrows():
        move1 = OwnMove(row['move1'], row['move1_type'], row['move1_power'], row['move1_accuracy'], row['max_pp1'], row['move1_pp'])

        stats = {'hp':row['max_hp'], 'atk':row['atk'], 'def':row['defe'], 'spa':row['spa'], 'spd':row['spd'], 'spe':row['spe'] }
        party.append(OwnPokemon(row['own_pokemon_name'], row['type1'], row['type2'], stats, move1, current_hp = row['hp'], status = row['status']))

