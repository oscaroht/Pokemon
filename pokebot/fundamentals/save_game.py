
from pokebot.fight import OwnPokemon
from pokebot.gameplay.item import Items
from sqlalchemy import create_engine
from .config import config
import os

def save_game_in_database(f, slot):
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    engine = create_engine(
        f"postgresql+psycopg2://postgres:{config('../../users.ini', 'postgres', 'password')}@localhost/pokemon")

    pokemon_queries = ''
    for p in OwnPokemon.all:

        empty_moves = ['-1',"-1",'-1','-1']
        pp = ['null', 'null', 'null', 'null']
        for i, m in enumerate(p.moves):
            empty_moves[i] = str(m.id)
            pp[i] = str(m.pp)
        moves_query = ', '.join(empty_moves) + ', ' + ', '.join(pp)

        single_pokemon_query = f"""insert into mart.own_pokemon(pokemon_id,own_pokemon_name,lvl,status,hp,max_hp,atk,defe,spa,spd,spe,move1_id,move2_id,move3_id,move4_id,move1_pp,move2_pp,move3_pp,move4_pp, saved_game_id)
        values ({p.pokemon_id},'{p.own_name}',{p.level},'{p.status}',{p.current_hp},{p.stats['hp']},{p.stats['atk']},{p.stats['def']},{p.stats['spa']},{p.stats['spd']},{p.stats['spe']},{moves_query}, v_saved_game_id) returning own_pokemon_id into v_own_pokemon_id;
        """
        pokemon_queries += single_pokemon_query
        if p in OwnPokemon.party:
            position = OwnPokemon.party.index(p)
            party_query = f"""insert into mart.party(saved_game_id, party_position, own_pokemon_id) 
                            values (v_saved_game_id, {position}, v_own_pokemon_id);
                            """
            pokemon_queries += party_query

    item_queries = ''
    for i in Items:
        if i.amount>0:
            item_queries += f""" insert into vault.own_items(item_id, item_name, amount, saved_game_id)
                    values ({i.id}, '{i.name}', {i.amount}, v_saved_game_id); """



    transaction = f"""
            begin;
            do
            $$
            declare
             v_saved_game_id int;
             v_own_pokemon_id int;
            begin
                insert into mart.saved_game(file_name, slot) values ('{f}', {slot})
                on conflict on constraint saved_unique do update set file_name = excluded.file_name, slot = excluded.slot
                returning saved_game_id into v_saved_game_id;
                
                delete from mart.own_pokemon where saved_game_id = v_saved_game_id;
                delete from vault.own_items where saved_game_id = v_saved_game_id;
                delete from mart.party where saved_game_id = v_saved_game_id;
                
                {pokemon_queries}

                {item_queries}
                
            end;
            $$;
            commit;
            """
    with engine.connect() as con:
        con.execute(transaction)

# save_game('test', 1)