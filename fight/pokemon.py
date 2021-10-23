
from sqlalchemy import create_engine
from fundamentals.config import config
import os
import pandas as pd

class PP_below_zero(Exception):
    pass

class InvalidPartyError(Exception):
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


    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    engine = create_engine(f"postgresql+psycopg2://postgres:{config('../users.ini','postgres','password')}@localhost/pokemon")

    with engine.connect() as con:
        pokemon_dict ={}
        temp = {}
        for row in con.execute(f"select * from mappings.pokemon;"):
            # get all the atributes in a dict instead of a tuple
            temp = dict((key, value) for key, value in row.items())
            # create 2 keys on pokemon_id and on pokemon_name
            pokemon_dict[row['pokemon_id']] = temp
            pokemon_dict[row['pokemon_name']] = temp

        for row in con.execute(f"select * from mappings.pokemon_move;"):
            Move( id =row['move_id'],
                  name = row['move_name'],
                  type1 = row['move_type'],
                  power=row['move_power'],
                  accuracy = row['move_accuracy'],
                  max_pp = row['max_pp'])

        df_pokemon = pd.read_sql_table('pokemon', con=con, schema='mappings', index_col='pokemon_id')
        df_moves = pd.read_sql_table('pokemon_move', con=con, schema='mappings', index_col='move_id')
        df_strength_weakness = pd.read_sql_table('strength_weakness', con=con, schema='mart')

        # for internal use. down here
        df_own_pokemon = pd.read_sql(query, con=con)

        # I have a separate data holder for these..
        #df_party = pd.read_sql_table('party', con=con, schema='mart')
        #df_own_pokemon = pd.read_sql_table('own_pokemon', con=con, schema='mart')


    own_pokemon = AllOwnPokemon()
    for index, row in df_own_pokemon.iterrows():
        move1 = OwnMove(row['move1_id'], row['move1'], row['move1_type'], row['move1_power'], row['move1_accuracy'],
                        row['max_pp1'], row['move1_pp'])
        move2 = OwnMove(row['move2_id'], row['move2'], row['move2_type'], row['move2_power'], row['move2_accuracy'],
                        row['max_pp2'], row['move2_pp'])
        move3 = OwnMove(row['move3_id'], row['move3'], row['move3_type'], row['move3_power'], row['move3_accuracy'],
                        row['max_pp3'], row['move3_pp'])
        move4 = OwnMove(row['move4_id'], row['move4'], row['move4_type'], row['move4_power'], row['move4_accuracy'],
                        row['max_pp4'], row['move4_pp'])
        moves = []
        for m in [move1,move2,move3,move4]:
            if m.id != -1:
                moves.append(m)


        stats = {'hp': row['max_hp'], 'atk': row['atk'], 'def': row['defe'], 'spa': row['spa'], 'spd': row['spd'],
                 'spe': row['spe']}

        own_pokemon.append(OwnPokemon(row['pokemon_id'], row['own_pokemon_name'], row['type1'], row['type2'], stats,
                                      row['own_pokemon_id'], row['own_pokemon_name'], row['lvl'], moves,
                                      current_hp=row['hp'], status=row['status']))
    party = Party()  # create empty party
    for index, row in df_own_pokemon.iterrows():
        own_id = row['own_pokemon_id']
        party.add(own_pokemon.get_pokemon_by_id(own_id))
    return party, own_pokemon, df_pokemon, df_moves, df_strength_weakness, pokemon_dict

class Move:

    all = {'id':{}, 'name':{}}

    def __init__(self, id,name, type1, power, accuracy, max_pp, adding=True):
        self.id = id
        self.name = name
        self.type = type1
        self.power = power
        self.accuracy = accuracy
        self.max_pp = max_pp
        if adding:
            Move.all['name'][name] = self
            Move.all['id'][id] = self

    @classmethod
    def get_move_by_id(cls, id):
        return cls.all['id'][id]

    @classmethod
    def get_move_by_name(cls, name):
        return cls.all['name'][name]


class OwnMove(Move):

    def __init__(self, id, name, type1, power, accuracy, max_pp, pp):
        super(OwnMove,self).__init__(id, name, type1, power, accuracy, max_pp, adding=False)
        self.pp = pp

    def lower_pp(self):
        if self.pp > 0:
            self.pp -=1
        else:
            raise PP_below_zero()


class Pokemon:

    _pokemon_dict = {'id':{},'name':{}}

    def __init__(self,pokemon_id, pokemon_name, type1, type2, base_stats, adding=True):#, base_stats):
        self.pokemon_id = pokemon_id
        self.name = pokemon_name
        self.type1 = type1
        self.type2 = type2
        self.base_stats = base_stats # dict {'hp':82, 'atk':50, ...}
        #self.evolve = evolve # dict {'method':'level', 'by': 16, 'into_name': 'Charmeleon'}
        if adding:
            self._add_to_dict()

    def _add_to_dict(self):
        print(Pokemon._pokemon_dict)
        Pokemon._pokemon_dict['id'][self.pokemon_id] = self
        Pokemon._pokemon_dict['name'][self.pokemon_name] = self

    @classmethod
    def get_pokemon_by_id(cls, id):
        return cls._pokemon_dict['id'][id]

    @classmethod
    def get_pokemon_by_name(cls, name):
        return cls._pokemon_dict['name'][name]

class WildPokemon(Pokemon):

    def __init__(self,pokemon_id, pokemon_name, type1, type2, base_stats, level):
        super(WildPokemon, self).__init__(pokemon_id, pokemon_name, type1, type2, base_stats, adding=False)

        self.level = level

        hp = int( (base_stats['hp'] * 2 * level)/100 + level + 10 )

        def other_stats(a):
            return int(base_stats[a] * 2 * level)/100 + 5

        self.stats = {'hp': hp,
                      'atk': other_stats('atk'),
                      'def': other_stats('def'),
                      'spa': other_stats('spa'),
                      'spd': other_stats('spa'),
                      'spe': other_stats('spe')}


class OwnPokemon(Pokemon):

    all = []

    def __init__(self,pokemon_id, pokemon_name, type1, type2, stats, own_id,own_name,level, own_moves, current_hp = 0, status = 'normal'): # add some kind of move id or move object
        super(OwnPokemon, self).__init__(pokemon_id, pokemon_name, type1, type2, stats, adding= False)

        self.own_id = own_id
        self.own_name =own_name
        # if you dont know (after caught) set stats to base_stats * level function and current_hp = 0
        self.stats = stats
        self.current_hp = current_hp
        self.status = status
        self.level = level

        # self.move1 = own_moves[0]
        # self.move2 = own_moves[1]
        # self.move3 = own_moves[2]
        # self.move4 = own_moves[3]

        self.moves = own_moves #[self.move1, self.move2, self.move3, self.move4]

        OwnPokemon.all.append(self)

    def heal(self):
        # self.move1.pp = self.move1.max_pp
        # self.move2.pp = self.move2.max_pp
        # self.move3.pp = self.move3.max_pp
        # self.move4.pp = self.move4.max_pp
        for m in self.moves:
            m.pp = m.max_pp
        self.current_hp = self.stats['max_hp']

    def level_up(self, new_level,hp, atk, defe, spa, spe):
        if new_level != self.level + 1:
            raise Exception('Not +1 level')
        self.level += 1
        # update stats
        self.stats = {'hp':hp, 'atk':atk, 'def':defe, 'spa':spa, 'spd':spa, 'spe':spe }

    def save(self):
        query =f"""insert into mart.own_pokemon values ({self.own_id}, {self.pokemon_id},'{self.own_name}',{self.level},'{self.status}',{self.current_hp},{self.stats['hp']},{self.stats['atk']},{self.stats['def']},{self.stats['spa']},{self.stats['spd']},{self.stats['spe']},{self.move1.id},{self.move2.id},{self.move3.id}, {self.move4.id}, {self.move1.max_pp}, {self.move2.max_pp}, {self.move3.max_pp}, {self.move4.max_pp})
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

    def add_move(self, m, i=5):
        if isinstance(m, OwnMove):
            if len(self.moves) < 4:
                self.moves.append(m)
                return
            if len(self.moves) == 4 and i <= 4:
                self.moves[i] = m
                return
            elif len(self.moves) == 4 and i > 4:
                print('ERROR: use the i argument the set the position on which this move should be placed.')
                return
            print(f'ERROR trying to add a move on index {i} but failed.')
        else:
            print('ERROR: argument should be instance of OwnMove.')

@singleton
class AllOwnPokemon(list):

    def get_pokemon_by_id(self,own_id):
        for i in range(len(self)):
            if self[i].own_id == own_id:
                return self[i]

@singleton
class Party(list):
    ''' This is a list containing the party. It cannot exceed length 6 since a party cannot hold more than 6 Pokemon.
    Also, only OwnPokemon object can populate the Party. The index of the list is the position in the party the pokemon
    is in. '''

    def add(self, pokemon):
        if len(self) < 6:
            self.append(pokemon)
        else:
            raise InvalidPartyError('Already 6 pokemon in party.')

    def rmv(self, pokemon): # remove is a list function
        if len(self.party) > 1:
            if pokemon in self:
                index = self.index(pokemon)
                self.pop(index)
            else:
                raise InvalidPartyError('Pokemon not found in party.')
        else:
            raise InvalidPartyError('Not enough pokemon in party to remove one.')

    def switch_position(self, pokemon, position = 0):
        if pokemon in self:
            old_position = self.index(pokemon)
            self.insert(position,self.pop(old_position))
        else:
            raise InvalidPartyError('Pokemon not found in party.')

    def heal(self):
        ''' Heal all pokemon in the party '''
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


# LOAD

party, own_pokemon, df_pokemon, df_moves, df_strength_weakness, pokemon_dict = load_pokemon()


if __name__=='__main__':

    test=1

