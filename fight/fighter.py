from fundamentals import FightState, state_check, screen_grab, goleft,goup,godown,goright,btnA,btnB
from fight.fight_rec import FightRec
#import fight_rec
from fight.pokemon import pokemon_dict, WildPokemon, df_strength_weakness, OwnPokemon, Move, OwnMove

import difflib
import numpy as np
import time

class FightMenuState(FightState):
    pass

class FoePokemonNotFound(Exception):
    pass

class Fight(): # Maybe we need to inherit OwnPokemon so the OwnPokemon objects get updated when changed.
    ''' A fight is defined as two pokemon in battle. On pokemon is your own, the other the foe. When one pokemon exits
    the fight the fight is over. Another pokemon might occur. This is a new fight and the Fight class is instanciated
    again.

    we can have several modes: 'max_damage', 'save_pp', 'catch', 'save_hp'
      these modes determine how we play.'''

    state = 'menu'

    def __init__(self):
        ''' construct the foe'''

        foe_level = FightRec.read_foe_level()

        foe_name_text = FightRec.read_foe_name().lower()
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

        self.foe_hp_fraction = FightRec.foe_hp()
        print(f'set my pokemon to {OwnPokemon.party[0].name}')
        self.my_pokemon = OwnPokemon.party[0]

        Fight.state = 'menu'

    # @classmethod
    # @state_check(FightState)
    # def set_state(cls, threshold = 0.5):
    #     screen = screen_grab(resize=True)
    #     # evaluate all templates
    #     best_score = 1
    #     for t in f_temp_list:
    #         if t.group == 'states':
    #             if t.mask is not None:
    #                 res = cv2.matchTemplate(screen, t.img, cv2.TM_SQDIFF_NORMED, mask=t.mask)
    #             else:
    #                 res = cv2.matchTemplate(screen, t.img, cv2.TM_SQDIFF_NORMED)
    #             min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    #             if min_val < best_score:  # lowest score is the best for SQDIFF
    #                 best_score = min_val
    #                 t_best = t
    #     if best_score > threshold:  # lowest score is the best for SQDIFF
    #         print('No orientation found.')
    #         return None
    #     print(f'{t_best.name} with a score of {best_score}')
    #     cls.state = t_best.option
    #     return t_best.option

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
        random = 235.5 / 254  # this is a normally distributed range between 217 and 254 divided by 254. So on average
                                # it is 235.5/254

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

        print(f"Move {move.name} has power {move.power} with my_pokemon has level {self.my_pokemon.level} and attack "
              f"{self.my_pokemon.stats['atk']} and spa {self.my_pokemon.stats['spa']}. Foe def {self.foe.stats['def']}"
              f"and spd {self.foe.stats['spd']}. Modifier {modifier}")

        return damage


    def calculate_best_move(self, mode = 'max_damage'):
        d = []
        print(f"Pokemon {self.my_pokemon.name}'s moves are {[x.name for x in self.my_pokemon.moves]}")
        for i in range(len(self.my_pokemon.moves)):
            if self.my_pokemon.moves[i].pp == 0:
                d += [-1] # lets append -1 so this move is not chosen
            elif self.my_pokemon.moves[i].power == 0:
                d += [0] # the _calculate_damage equation becomes slightly positive so lets set it back to 0
            else:
                d += [self._calculate_damage(self.my_pokemon.moves[i])]
        print(f"with expected damages: {d}")

        if mode == 'max_damage':
            return np.argmax(d), max(d) # so argmax 0 becomes move 1
        elif mode == 'catch':
            hp_fraction = FightRec.foe_hp() # check the foes current hp
            hp = hp_fraction * self.foe.stats['hp']
            print(f"Estimated hp: {hp}  with max hp: {self.foe.stats['hp']}")
            for i in range(len(d)):
                if d[i] > hp: # if the attack does more damage than the hp do not use it
                    d[i] = -2
            return np.argmax(d), max(d)

    def execute_best_move(self, mode='max_damage'):
        ''' mode can be 'best', 'save_pp' '''
        from fight.selector import Selector

        d = []
        print(f"Pokemon {self.my_pokemon.name}'s moves are {[x.name for x in self.my_pokemon.moves]}")
        for i in range(len(self.my_pokemon.moves)):
            if self.my_pokemon.moves[i].pp == 0:
                d += [-1] # lets append -1 so this move is not chosen
            elif self.my_pokemon.moves[i].power == 0:
                d += [0] # the _calculate_damage equation becomes slightly positive so lets set it back to 0
            else:
                d += [self._calculate_damage(self.my_pokemon.moves[i])]
        print(f"with expected damages: {d}")

        if mode == 'max_damage':
            if max(d) > 0:
                move_idx = np.argmax(d) # so argmax 0 becomes move 1
                self._perform_move(move_idx)
            else:
                print("No damaging move left")
        elif mode == 'catch':
            hp_fraction = FightRec.foe_hp() # check the foe's current hp
            hp = hp_fraction * self.foe.stats['hp']
            print(f"Estimated hp: {hp}  with max hp: {self.foe.stats['hp']}")
            max_idx = None
            max_dam = 0
            for i, md in enumerate(d):
                if hp > md > 0:  # a valid move does damage (md > 0) and does not eliminate the foe (md < hp)
                    if md > max_dam: # check if this valid move is also the one with most damage
                        max_idx = i
                        max_dam = md
            if max_idx != None:
                self._perform_move(max_idx)
            else:
                print("throw ball")
                Selector.use_item('pokeball')


    def _perform_move(self, idx):
        from .selector import Selector
        # select the best move Selector
        Selector.select_move_by_idx(idx)

        # lower the pp in the move object associated with the pokemon
        self.my_pokemon.moves[idx].lower_pp()
        # set the state to a waiting state
        Selector.state = None

    def _bar_stat_fell(self,text):
        return
    def _bar_enemy_fainted(self):
        # delete Fight object
        return
    def _bar_exp_gained(self):
        return
    def _bar_wild_pokemon_appeared(self):
        return
    def _bar_go_my_pokemon(self):
        return
    def _bar_critical_hit(self):
        return
    def _bar_level_up(self, text):
        import re
        hp_bar = FightRec.read_hp()
        hp_max = re.split('/|z', '28z28')[1]  # sometimes / is mistaken by z
        self.my_pokemon.stats['hp'] = int(hp_max)

        new_level = re.sub('[^\d{1,3}]', '', text)         # I match with 3 because sometimes the ! is seen as a \d. I remove this later
        new_level = int( new_level[0:2] )

        current_level = self.my_pokemon.level
        if new_level == current_level + 1:
            # this is expected
            self.my_pokemon.level = new_level
        elif new_level[0] == current_level+1:
            # the ! is probably replaced with a \d and because we are in single digit levels new_level[0:2] does not remove the errorous !
            self.my_pokemon.level = new_level[0]

        time.sleep(1) # takes a little time before the stats update window appears

        new_stats = FightRec.read_stat_update()
        self.my_pokemon.stats['atk'] = new_stats['attack']
        self.my_pokemon.stats['def'] = new_stats['defense']
        self.my_pokemon.stats['spe'] = new_stats['speed']
        self.my_pokemon.stats['spd'] = new_stats['special']
        self.my_pokemon.stats['spa'] = new_stats['special']

    def _bar_new_move_learned(self,text):
        ''' this function used the difflib to figure out what move it is.'''
        from .pokemon import Move, OwnMove
        from .selector import Selector
        import re

        t = text.replace(self.my_pokemon.name.upper(), '')
        t = re.sub('[^A-Z]*', '', t)

        new_move_name = difflib.get_close_matches(t, [str(x).upper() for x in list(Move.all['name'].keys())], n=1)[0]
        new_move = Move.get_move_by_name(new_move_name.lower())
        new_own_move = OwnMove(new_move.id, new_move.name, new_move.type, new_move.power, new_move.accuracy, new_move.max_pp, new_move.max_pp)
        '''' if we have less than 4 moves we can just add it '''
        if len(self.my_pokemon.moves) < 4:
            self.my_pokemon.add_move(new_own_move)
        else:
            print('TO DO add handling of replacing a move')



    def interpret_bar(self, text):
        '''' instead of a string we could return functions depending on what needs to be done '''

        if 'Enem' in text and 'fainted' in text:
            return self._bar_enemy_fainted()
        elif 'gain' in text and 'EXP' in text:
            return self._bar_exp_gained()
        elif 'appeared' in text:
            return self._bar_wild_pokemon_appeared()
        elif 'Go!' in text:
            return self._bar_go_my_pokemon()
        elif 'used' in text:
            return 'move_used'
        elif 'Critical hit' in text:
            return 'critical_hit'
        elif 'Enem' in text and 'fell' in text:
            print('fight: ENEMY DEFEATED')
            return 'enemy_stat_fell'
        elif 'learn' in text:
            print('fight: NEW MOVE LEARED!')
            return self._bar_new_move_learned(text)
        elif 'level' in text:
            print('fight: LEVEL UP')
            return self._bar_level_up(text)
        elif 'fell' in text:
            print('fight: STATS FELL' )
            return self._bar_stat_fell(text)
        elif 'wascaught' in text:
            print('fight: FOE CAUGHT')
            return self.foe.caught()
        elif 'nickname' in text:
            return btnB()


class Fighter:


    @classmethod
    def eval_pokemon_stats(cls):
        from fight.selector import Selector
        idx = OwnPokemon.party.stats_need_evaluation(return_party_idx = True)
        print(f"Doing the evaluation in fighter for idx {idx}")
        if idx == None:
            # print("eval_pokemon_stats needed says SC but no pokemon was found which need evaluation")
            raise Exception("eval_pokemon_stats needed says SC but no pokemon was found which need evaluation")
        print(f"Go to stats page of game menu for pokemon {idx}")
        Selector.eval_pokemon_stats_by_idx(idx)  # bring us to the stats page in the game menu
        # read the values
        stats = FightRec.read_stat_gm_lookup()
        hp_current, hp_max = FightRec.read_stat_gm_hp()
        stats['hp'] = hp_max
        # update pokemon object
        OwnPokemon.party[idx].stats = stats
        OwnPokemon.party[idx].current_hp = hp_current

        test=1

        #evaluate moves
        if OwnPokemon.party[idx].moves == []:
            Selector.eval_pokemon_moves_by_idx(idx)
            moves = FightRec.read_moves_gm()
            for m in moves:
                new_own_m = OwnMove.create_own_move_by_name(m) # also a name that is similar, reading mistakes allowed
                OwnPokemon.party[idx].add_move(new_own_m)


    @classmethod
    def handle_fight(cls, mode = 'max_damage'):
        from fundamentals import StateController
        from fight.selector import Selector
        from fundamentals import btnA

        # first lets check again
        StateController.eval_state()
        sn = StateController.state_name()
        while 'fight' in sn or 'none' in sn:
            StateController.eval_state()
            sn = StateController.state_name()
            print(f'State name {StateController.state_name()}')
            if StateController.state_name() == 'fight_init':
                Selector.init_fight()
            elif not ('f' in globals() or 'f' in locals()):
                # so the fight was not yet initiated
                f = Fight()
            elif StateController.state_name() == 'fight_pokedex':
                '''' A new pokemon was recently caught. Besides skipping the pokedex window we should add it to our 
                party'''

                print("handle pokedex state")

                # maybe add the foe to the party or PC and leave out the needed info. make a state that checks if the
                # info of all pokemon present and if that is not the case it goes and checks it. This state is a
                # substate of the walk state as we can only check the states from the game menu (ony accessible when the
                # player is visible or in the walk state)

                # ISSUE this should not be done in the pokedex state because if a pokemon is caught for the 2nd time the
                # pokedex will not pop up. So we need to create a obtain pokemon function which is called/ triggered by
                # the text in the bar. But it is always the end of the fight.

                #f.foe.caught() # add foe to own pookemon

                for i in range(3):
                    print("Bash B")
                    btnB()
                    time.sleep(1)
                    btnB()
                StateController.eval_state()

            elif StateController.state_name() == 'fight_wait_arrow':
                text = FightRec.read_bar()
                # interpret text
                print(text)
                f.interpret_bar(text)
                btnA()
                time.sleep(0.3)
            elif StateController.state_name() in ['fight_menu', 'fight_item', 'fight_pokemon','fight_move']:
                # we are in the main fight
                f.execute_best_move(mode=mode)



if __name__ == '__main__':
    Fighter.eval_pokemon_stats()
    test=1

