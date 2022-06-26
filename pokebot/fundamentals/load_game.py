import os
import sqlalchemy
import pandas as pd

from pokebot.fight.pokemon import OwnMove, OwnPokemon, Pokemon, Move
from pokebot.gameplay.item import Item, Items
from .config import config


def load_game(filename):
    OwnPokemon.new_game()
    Items.new_game()

    query = f"""select 
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
    join mappings.pokemon_move f on a.move4_id = f.move_id
    join mart.saved_game g on a.saved_game_id = g.saved_game_id
	join mart.party h on a.saved_game_id = h.saved_game_id and a.own_pokemon_id = h.own_pokemon_id 
    where g.file_name = '{filename}'
    order by h.party_position asc;
     """

    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    engine = sqlalchemy.create_engine(
        f"postgresql+psycopg2://postgres:{config('../../users.ini', 'postgres', 'password')}@localhost/pokemon")

    with engine.connect() as con:
        party_id_list = [row['own_pokemon_id'] for row in con.execute(f"select * from mart.party;")]
        # own_pokemon = AllOwnPokemon()
        for row in con.execute(query):
            move1 = OwnMove(row['move1_id'], row['move1'], row['move1_type'], row['move1_power'], row['move1_accuracy'],
                            row['max_pp1'], row['move1_pp'])
            move2 = OwnMove(row['move2_id'], row['move2'], row['move2_type'], row['move2_power'], row['move2_accuracy'],
                            row['max_pp2'], row['move2_pp'])
            move3 = OwnMove(row['move3_id'], row['move3'], row['move3_type'], row['move3_power'], row['move3_accuracy'],
                            row['max_pp3'], row['move3_pp'])
            move4 = OwnMove(row['move4_id'], row['move4'], row['move4_type'], row['move4_power'], row['move4_accuracy'],
                            row['max_pp4'], row['move4_pp'])
            moves = []
            for m in [move1, move2, move3, move4]:
                if m.id != -1:
                    moves.append(m)

            stats = {'hp': row['max_hp'], 'atk': row['atk'], 'def': row['defe'], 'spa': row['spa'], 'spd': row['spd'],
                     'spe': row['spe']}

            if row['own_pokemon_id'] in party_id_list:
                ip = True
            else:
                ip = False

            OwnPokemon(row['pokemon_id'], row['own_pokemon_name'], row['type1'], row['type2'], stats,
                       row['own_pokemon_id'], row['own_pokemon_name'], row['lvl'], moves,
                       current_hp=row['hp'], status=row['status'], in_party=ip)

    with engine.connect() as con:
        query = f"""select * from vault.own_items a
                    join mart.saved_game b on a.saved_game_id = b.saved_game_id
                    where b.file_name = '{filename}';"""
        for row in con.execute(query):
            Items.get_item_by_id(row['item_id']).amount = row['amount']

if __name__ == '__main__':
    load_game('Pokemon Blue8.sgm')