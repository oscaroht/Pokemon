from fundamentals import FightState, state_check, screen_grab, goleft,goup,godown,goright,btnA,btnB
from fight_ocr import FightOCR
from pokemon import pokemon_dict, WildPokemon, party, df_strength_weakness
from templates import f_temp_list
import difflib
import cv2
import numpy as np
import time

class FightMenuState(FightState):
    pass

class FoePokemonNotFound(Exception):
    pass

class Fight:
    ''' A fight is defined as two pokemon in battle. On pokemon is your own, the other the foe. When one pokemon exits
    the fight the fight is over. Another pokemon might occur. This is a new fight and the Fight class is instanciated
    again.'''

    state = 'menu'

    def __init__(self):
        ''' construct the foe'''

        foe_level = FightOCR.read_foe_level()

        foe_name_text = FightOCR.read_foe_name().lower()
        foe_name = difflib.get_close_matches(foe_name_text, [str(x) for x in list(pokemon_dict.keys())] , n=1)
        if len(foe_name)==0:
            raise FoePokemonNotFound
        foe_name =foe_name[0] # extract the best match

        s = pokemon_dict[foe_name]
        self.foe = WildPokemon(s['pokemon_id'],
                      s['pokemon_name'],
                      s['type1'],
                      s['type2'],
                      {'hp':s['base_hp'],
                            'atk':s['base_atk'],
                            'def':s['base_def'],
                            'spa':s['base_spa'],
                            'spd':s['base_spa'],
                            'spe':s['base_spe'] } ,
                      int(foe_level) )

        self.my_pokemon = party[0]

        Fight.state = 'menu'

    @classmethod
    @state_check(FightState)
    def set_state(cls, threshold = 0.5):
        screen = screen_grab(resize=True)
        # evaluate all templates
        best_score = 1
        for t in f_temp_list:
            if t.group == 'states':
                if t.mask is not None:
                    res = cv2.matchTemplate(screen, t.img, cv2.TM_SQDIFF_NORMED, mask=t.mask)
                else:
                    res = cv2.matchTemplate(screen, t.img, cv2.TM_SQDIFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                if min_val < best_score:  # lowest score is the best for SQDIFF
                    best_score = min_val
                    t_best = t
        if best_score > threshold:  # lowest score is the best for SQDIFF
            print('No orientation found.')
            return None
        print(f'{t_best.name} with a score of {best_score}')
        cls.state = t_best.option
        return t_best.option

    def _calculate_damage(self, move):
        if move.id == -1:
            return 0

        special_moves = ['water', 'grass', 'fire', 'ice', 'electric', 'psychic']
        physical_moves = ['normal', 'fighting', 'flying', 'ground', 'rock', 'bug', 'ghost', 'poison']

        if move.type == self.my_pokemon.type1 or move.type == self.my_pokemon.type2:
            stab = 1.5  # same type attack bonus (stab)
        else:
            stab = 1

        multiplier = df_strength_weakness[
            (df_strength_weakness['atk'] == move.type) & (df_strength_weakness['def'] == self.foe.type1)].iloc[0][
            'multiplier']  # has to be iloc instead of loc because we are not using the indexes
        if self.foe.type2 != '-':
            multiplier_2 = df_strength_weakness[
                (df_strength_weakness['atk'] == move.type) & (df_strength_weakness['def'] == self.foe.type2)].iloc[0][
                'multiplier']  # has to be iloc instead of loc because we are not using the indexes
            multiplier *= multiplier_2
        random = int(235.5 / 254)  # this is a normally distributed range between 217 and 254 divided by 254

        modifier = random * multiplier * stab

        critical = 1  # if it is a critical hit this should be 2

        """" from https://bulbapedia.bulbagarden.net/wiki/Damage#Damage_calculation
         the 100/50 gives special moves such as growl also damage. Which should not be the case."""
        if move.type in special_moves:
            damage = (((2 / 5) * self.my_pokemon.level * critical + 2) * move.power * self.my_pokemon.stats['spa'] /
                      self.foe.stats['spd'] + 100) / 50 * modifier
        elif move.type in physical_moves:
            damage = (((2 / 5) * self.my_pokemon.level * critical + 2) * move.power * self.my_pokemon.stats['atk'] /
                      self.foe.stats['def'] + 100) / 50 * modifier
        else:
            raise Exception(f'Move type {move.type} unknown.')

        return damage

    def calculate_best_move(self):
        d = []
        for i in range(4):
            if self.my_pokemon.moves[i].id != -1 and self.my_pokemon.moves[i].pp > 0:     # nice conditionals are checked one at a time
                d += [ self._calculate_damage(self.my_pokemon.moves[i]) ]

        # d2 = calculate_damage(my_pokemon, my_pokemon.move2, foe)
        # d3 = calculate_damage(my_pokemon, my_pokemon.move3, foe)
        # d4 = calculate_damage(my_pokemon, my_pokemon.move4, foe)
        return np.argmax(d) # so argmax 0 becomes move 1


if __name__ == '__main__':

    f = Fight()

    pass