import difflib
import numpy as np
import time

from ..fundamentals import FightState
from ..fundamentals import btnA,btnB
from .fight_rec import FightRec
from .pokemon import OwnPokemon, WildPokemon, Pokemon, OwnMove, Move
from .selector import Selector

import logging
logger = logging.getLogger(__name__)

class FightMenuState(FightState):
    pass

class FoePokemonNotFound(Exception):
    pass
class FoePokemonNotFoundInBar(Exception):
    pass


class Fight(): # Maybe we need to inherit OwnPokemon so the OwnPokemon objects get updated when changed.
    ''' A fight is defined as two pokemon in battle. On pokemon is your own, the other the foe. When one pokemon exits
    the fight the fight is over. Another pokemon might occur. This is a new fight and the Fight class is instanciated
    again.

    we can have several modes: 'max_damage', 'save_pp', 'catch', 'save_hp'
      these modes determine how we play.'''

    def __init__(self, my_pokemon=OwnPokemon.party[0]):
        ''' construct the foe'''
        self.foe_def = False
        self.next_foe_name = None

        self.my_pokemon = my_pokemon

        foe_level: str = FightRec.read_foe_level()
        if foe_level.isdigit():
            foe_level = int(foe_level)
        else:
            foe_level = 99  # if unknown assume it is very high

        foe_name: str = Pokemon.get_closest_match_by_name(FightRec.read_foe_name().lower())
        pokemon_obj: Pokemon = Pokemon.get_pokemon_by_name(foe_name)
        self.foe = WildPokemon.build_from_pokemon_object(pokemon_obj, foe_level)
        self.foe_hp_fraction: int = FightRec.foe_hp()
        logger.info(f'Foe.name: {foe_name}, foe.level: {foe_level}')
        logger.info(f'My_pokemon.name: {my_pokemon}')

    def _calculate_damage(self, move):
        if move.id == -1:
            return 0

        special_moves = ['water', 'grass', 'fire', 'ice', 'electric', 'psychic']
        physical_moves = ['normal', 'fighting', 'flying', 'ground', 'rock', 'bug', 'ghost', 'poison']

        if move.type == self.my_pokemon.type1 or move.type == self.my_pokemon.type2:
            stab = 1.5  # same type attack bonus (stab)
        else:
            stab = 1

        multiplier = Pokemon.df_strength_weakness[
            (Pokemon.df_strength_weakness['atk'] == move.type) & (Pokemon.df_strength_weakness['def'] == self.foe.type1)].iloc[0][
            'multiplier']  # has to be iloc instead of loc because we are not using the indexes
        if self.foe.type2 != '-':
            multiplier_2 = Pokemon.df_strength_weakness[
                (Pokemon.df_strength_weakness['atk'] == move.type) & (Pokemon.df_strength_weakness['def'] == self.foe.type2)].iloc[0][
                'multiplier']  # has to be iloc instead of loc because we are not using the indexes
            multiplier *= multiplier_2
        random = 235.5 / 254  # this is a normally distributed range between 217 and 254 divided by 254. So on average
                                # it is 235.5/254

        modifier = random * multiplier * stab

        critical = 1  # if it is a critical hit this value is 2. but there is now way to know beforehand

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

        logger.debug(f"Move {move.name} has power {move.power} with my_pokemon {self.my_pokemon.name} has level {self.my_pokemon.level} and attack "
              f"{self.my_pokemon.stats['atk']} and spa {self.my_pokemon.stats['spa']}. Foe {self.foe.name} def {self.foe.stats['def']}"
              f"and spd {self.foe.stats['spd']}. Modifier {modifier}")

        return damage


    # def calculate_best_move(self, mode = 'max_damage'):
    #     d = []
    #     logger.info(f"Pokemon {self.my_pokemon.name}'s moves are {[x.name for x in self.my_pokemon.moves]}")
    #     for i in range(len(self.my_pokemon.moves)):
    #         if self.my_pokemon.moves[i].pp == 0:
    #             d += [-1] # lets append -1 so this move is not chosen
    #         elif self.my_pokemon.moves[i].power == 0:
    #             d += [0] # the _calculate_damage equation becomes slightly positive so lets set it back to 0
    #         else:
    #             d += [self._calculate_damage(self.my_pokemon.moves[i])]
    #     logger.info(f"Expected damages: {d}")
    #
    #     if mode == 'max_damage':
    #         return np.argmax(d), max(d) # so argmax 0 becomes move 1
    #     elif mode == 'catch':
    #         hp_fraction = FightRec.foe_hp() # check the foes current hp
    #         hp = hp_fraction * self.foe.stats['hp']
    #         logger.info(f"Estimated hp: {hp}  with max hp: {self.foe.stats['hp']}")
    #         for i in range(len(d)):
    #             if d[i] > hp: # if the attack does more damage than the hp do not use it
    #                 d[i] = -2
    #         return np.argmax(d), max(d)

    def execute_best_move(self, mode='max_damage'):
        ''' mode can be 'best', 'save_pp' '''
        # from fight.selector import Selector
        if mode not in ['catch', 'max_damage']:
            raise Exception(f"Invalid input argument {mode}. Only allowed {['catch', 'max_damage']}")

        d = []
        logger.info(f"Pokemon {self.my_pokemon.name}'s moves are {[x.name for x in self.my_pokemon.moves]}")
        for i in range(len(self.my_pokemon.moves)):
            if self.my_pokemon.moves[i].pp == 0:
                d += [-1] # lets append -1 so this move is not chosen
            elif self.my_pokemon.moves[i].power == 0:
                d += [0] # the _calculate_damage equation becomes slightly positive so lets set it back to 0
            else:
                d += [self._calculate_damage(self.my_pokemon.moves[i])]
        logger.info(f"with expected damages: {d}")

        if mode == 'max_damage':
            if max(d) > 0:
                move_idx = np.argmax(d) # so argmax 0 becomes move 1
                self._perform_move(move_idx)
            else:
                logger.info("No damaging move left")
                logger.error("NOT IMPLEMENTED YET")
        elif mode == 'catch':
            from ..gameplay import Items
            hp_fraction = FightRec.foe_hp() # check the foe's current hp
            hp = hp_fraction * self.foe.stats['hp']
            logger.info(f"Estimated foe hp: {hp}  with max hp: {self.foe.stats['hp']}")
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
                logger.info("try to throw ball")
                balls = Items.get_item_by_name('poke ball')
                logger.info(f"Number of balls is {balls.amount}")
                Selector.use_item('poke ball')
                balls.lower_amount()
                logger.debug(f"Number after throwing a ball is {balls.amount}")

    def set_current_own_hp(self):
        current_hp, _ = self.eval_hp()
        self.my_pokemon.current_hp = current_hp

    def eval_hp(self):
        import re
        hp_bar = FightRec.read_hp()
        hps = re.split('/|z', hp_bar)  # sometimes / is mistaken by z
        return int(hps[0]), int(hps[1])

    def set_max_hp(self):
        _, hp_max = self.eval_hp()
        self.my_pokemon.stats['hp'] = hp_max

    def _perform_move(self, idx):
        # from fight.selector import Selector
        # select the best move Selector
        Selector.select_move_by_idx(idx)

        # lower the pp in the move object associated with the pokemon
        self.my_pokemon.moves[idx].lower_pp()
        # set the state to a waiting state
        Selector.state = None

    def _bar_next_pokemon(self,text):
        foe_name = text.split('use')[1][0:-1]
        foe_name = difflib.get_close_matches(foe_name.lower(), Pokemon.get_list_of_all_pokemon_names() , n=1)
        if len(foe_name)==0:
            return
            #raise FoePokemonNotFoundInBar
        logger.info(f"Next foe pokemon will be: {foe_name[0]}")
        self.next_foe_name = foe_name[0] # extract the best match

    def _bar_stat_fell(self,text):
        return
    def _bar_enemy_fainted(self):
        self.foe_def = True
        # delete Fight object
        return
    def _bar_exp_gained(self):
        self.foe_def = True
        return
    def _bar_wild_pokemon_appeared(self):
        return
    def _bar_go_my_pokemon(self):
        return
    def _bar_critical_hit(self):
        return
    def _bar_level_up(self, text):
        import re
        # hp_bar = FightRec.read_hp()
        # hp_max = re.split('/|z', hp_bar)[1]  # sometimes / is mistaken by z
        # self.my_pokemon.stats['hp'] = int(hp_max)

        # check which pokemon went a level up
        pokemon_name = difflib.get_close_matches(text.split('grew')[0].lower(),[p.own_name for p in OwnPokemon.party], n=1)[0]
        pokemon = OwnPokemon.party.get_own_pokemon_by_own_name(pokemon_name)

        pokemon.needs_hp_max_check = True

        new_level_str = re.sub('[^\d{1,3}]', '', text)         # I match with 3 because sometimes the ! is seen as a \d. I remove this later
        new_level_str_2 = new_level_str[0:2]
        new_level = int( new_level_str_2 )

        current_level = pokemon.level
        if new_level == current_level + 1:
            # this is expected
            pokemon.level = new_level
        elif new_level_str_2[0] == current_level+1:
            # the ! is probably replaced with a \d and because we are in single digit levels new_level[0:2] does not remove the errorous !
            pokemon.level = new_level[0]
        else:
            logger.warning(f"New level {new_level} does not seem right")

        time.sleep(1) # takes a little time before the stats update window appears

        new_stats = FightRec.read_stat_update()
        pokemon.stats['atk'] = new_stats['attack']
        pokemon.stats['def'] = new_stats['defense']
        pokemon.stats['spe'] = new_stats['speed']
        pokemon.stats['spd'] = new_stats['special']
        pokemon.stats['spa'] = new_stats['special']

        time.sleep(1)

    def _bar_new_move_learned(self,text):
        ''' this function used the difflib to figure out what move it is.'''
        # from .pokemon import Move, OwnMove
        # from .selector import Selector
        import re

        pokemon_name = \
        difflib.get_close_matches(text.split('learn')[0].lower(), [p.own_name for p in OwnPokemon.party], n=1)[0]
        pokemon = OwnPokemon.party.get_own_pokemon_by_own_name(pokemon_name)

        t = text.replace(pokemon_name.upper(), '')  # replace the pokemon name from the text
        t = re.sub('[^A-Z]*', '', t)  # take the upper case characters from the string

        logger.info(f"New move name: {t}")
        move_options = difflib.get_close_matches(t, [str(x).upper() for x in list(Move.all['name'].keys())], n=1)
        if len(move_options) == 0:
            raise Exception(f"No match found for move {t} for own pokemon {pokemon}")
        new_move_name = move_options[0]
        if new_move_name.lower() in [m.name for m in pokemon.moves]:
            logger.warning(
                f"Move {new_move_name} already in {pokemon.own_name.upper()}'s moves. Not allowed so we do not add it")
            return  # do not do anything if the pokemon already has the move
        new_move = Move.get_move_by_name(new_move_name.lower())
        new_own_move = OwnMove(new_move.id, new_move.name, new_move.type, new_move.power, new_move.accuracy,
                               new_move.max_pp, new_move.max_pp)
        '''' if we have less than 4 moves we can just add it '''
        if len(pokemon.moves) < 4:
            pokemon.add_move(new_own_move)
        else:
            logger.error('TO DO add handling of replacing a move')


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
            logger.debug('fight: ENEMY STATS FELL')
            return 'enemy_stat_fell'
        elif 'learn' in text:
            logger.info('NEW MOVE LEARED!')
            return self._bar_new_move_learned(text)
        elif 'level' in text:
            logger.info('LEVEL UP')
            return self._bar_level_up(text)
        elif 'fell' in text:
            logger.info('OWN STATS FELL' )
            return self._bar_stat_fell(text)
        elif 'wascaught' in text:
            logger.info('fight: FOE CAUGHT')
            return self.foe.caught()
        elif 'nickname' in text:
            logger.info("Press B to skip nickname")
            return btnB()
        elif 'about' in text and 'use' in text:
            return self._bar_next_pokemon(text)
        # elif 'evolving' in text:
        #     return self._bar_evolve()
        # elif 'change' in text and 'POK' in text:
        #     return Fighter.choose_new_pokemon('current_pokemon') # after interpret text A is clicked in the function\
        # we do not want this so we make an independent state




class Fighter:

    @classmethod
    def handle_talk(cls):
        btnA()

    @classmethod
    def eval_pokemon_stats(cls):
        '''' When a new pokemon is caught the stats are unknown. Therefore we need to get the stats via the menu '''

        # from fight.selector import Selector
        logger.debug(f"Check which pokemon needs stats eval")
        idx = OwnPokemon.party.stats_need_evaluation(return_party_idx = True)
        logger.debug(f"That pokemon is at idx {idx}")
        if idx is None:
            raise Exception("eval_pokemon_stats needed says SC but no pokemon was found which need evaluation")
        logger.debug(f"Go to stats page of game menu for pokemon {idx}")
        Selector.go_to_pokemon_stats_page_by_idx(idx)  # bring us to the stats page in the game menu
        # read the values
        stats = FightRec.read_stat_gm_lookup()
        hp_current, hp_max = FightRec.read_stat_gm_hp()
        stats['hp'] = hp_max
        # update pokemon object
        OwnPokemon.party[idx].stats = stats
        OwnPokemon.party[idx].current_hp = hp_current

        #evaluate moves
        if OwnPokemon.party[idx].moves == []:
            Selector.go_to_pokemon_moves_page_by_idx(idx)
            moves = FightRec.read_moves_gm()
            for m in moves:
                new_own_m = OwnMove.create_own_move_by_name(m) # also a name that is similar, reading mistakes allowed
                OwnPokemon.party[idx].add_move(new_own_m)
        else:
            btnB() # go to move page but do not do anything

        btnB(3) # exit move page, party menu, game menu

    # NOT USED
    @classmethod
    def put_pokemon_by_idx_in_front_of_party(cls, idx):
        # from fight.selector import Selector
        if idx == 0:
            logger.warning(f"Pokemon on idx 0 already in front of party")
            return
        elif idx > 6:
            raise Exception(f"Invalid argument {idx}. Party only has length 6. Unable to put pokemon from position 7")
        Selector.put_pokemon_idx_in_front(idx)
        OwnPokemon.party.switch_position(OwnPokemon.party[idx], new_position=0) # pokemon object, new position

    @classmethod
    def put_pokemon_in_front_of_party(cls, pokemon):
        # from fight.selector import Selector
        if pokemon == OwnPokemon.party[0]:
            return
        elif pokemon not in OwnPokemon.party:
            raise Exception(f"Pokemon {pokemon} not in party")
        logger.info(f"Put pokemon {pokemon.own_name} in front")
        idx = OwnPokemon.party.index(pokemon)
        Selector.put_pokemon_idx_in_front(idx)
        OwnPokemon.party.switch_position(pokemon, new_position=0) # pokemon object, new position


    @classmethod
    def choose_new_pokemon(cls, which):
        if which == 'current_pokemon':
            # time.sleep(0.5)
            logger.info("press B to keep current pokemon")
            btnB()
            # time.sleep(0.5)
        else:
            logger.error(f"Choosing another pokemon is not supported yet")


    @classmethod
    def handle_foe(cls, my_pokemon, wild=False, mode='max_damage'):
        from ..fundamentals import StateController
        # from fight.selector import Selector
        from pokebot.game_plan import Gameplan
        from ..gameplay import Items

        sn = StateController.eval_state()
        logger.debug(f'State name {StateController.state_name()}')

        while sn in ['fight_init', 'fright_init_trainer','fight_wait_arrow']:   # if we keep hanging in the init state than keep initting
            Selector.init_fight()
            sn = StateController.eval_state()

        StateController.in_fight = True
        f = Fight(my_pokemon)

        # print(f.foe.name in Gameplan.catch_pokemon)
        # print(OwnItems.do_i_have("Poke Ball"))
        # print(wild)
        # print(not OwnPokemon.do_i_have_pokemon_by_name(f.foe.name))
        if (f.foe.name in Gameplan.catch_pokemon) and Items.do_i_have("poke ball") and wild and (not OwnPokemon.do_i_have_pokemon_by_name(f.foe.name)):
            mode = 'catch'
        logger.debug(f'mode: {mode}')

        # sn = 'fight'
        while 'fight' in sn or 'none' in sn:
            if sn == 'fight_pokedex':
                '''' A new pokemon was recently caught. Besides skipping the pokedex window we should add it to our 
                party'''

                logger.debug("handle pokedex state")

                # maybe add the foe to the party or PC and leave out the needed info. make a state that checks if the
                # info of all pokemon present and if that is not the case it goes and checks it. This state is a
                # substate of the walk state as we can only check the states from the game menu (ony accessible when the
                # player is visible or in the walk state)

                # ISSUE this should not be done in the pokedex state because if a pokemon is caught for the 2nd time the
                # pokedex will not pop up. So we need to create a obtain pokemon function which is called/ triggered by
                # the text in the bar. But it is always the end of the fight.

                # f.foe.caught() # add foe to own pokemon

                for i in range(2):
                    logger.debug("Bash B")
                    btnB()
                    time.sleep(1)
                    btnB()
                StateController.eval_state()
                return
            elif StateController.wait_arrow:
                text = FightRec.read_bar()
                # interpret text
                logger.debug(text)
                f.interpret_bar(text)
                time.sleep(0.1) # need some time
                btnA()
                time.sleep(0.5)  # need some time for the text to disappear otherwise it is read twice and the next text will be skipped because A is pressed to quickly
            elif sn == 'fight_level_up':
                text = FightRec.read_bar()
                # interpret text
                logger.debug(text)
                #f.interpret_bar(text) # we can also call the interet bar function instead of directly calling _bar_level_up
                f._bar_level_up(text)
                btnA()
                time.sleep(0.5)  # need some time for the text to disappear otherwise it is read twice and the next text will be skipped because A is pressed to quickly

            elif sn == 'fight_change_pokemon':
                return f.next_foe_name # this pokemon fight has ended and we have all the after fight information (exp, lvl up, new stats, new moves)

            elif sn == 'fight_use_next_pokemon':
                # our pokemon was defeated
                # put hp to zero of current pokemon
                f.my_pokemon.current_hp = 0
                # yes we want to choose a new pokemon

                return # return without return arg so we are not choosing a new pokemon
            elif sn in ['fight_menu', 'fight_item', 'fight_pokemon', 'fight_move']:
                # we are in the main fight
                if f.foe_def: # if the foe was defeated we do not continue because there is a new foe
                    logger.debug("Foe is already eliminated so we exit and drop the f object")
                    return f.next_foe_name # this code flow is needed for when the pplayer only has 1 pokemon
                f.set_current_own_hp()
                if f.my_pokemon.needs_hp_max_check: # after level up we need to check the new max hp
                    f.set_max_hp()
                    f.my_pokemon.needs_hp_max_check = False
                if mode == 'catch' and not Items.do_i_have("poke ball"):
                    logger.info("No more pokeballs. Switch mode from catch to max damage")
                    mode = 'max_damage'
                elif mode == 'train':
                    # switch pokemon if foe is to strong. We choose the max level pokemon that is ready to fight
                    if f.my_pokemon.level <= f.foe.level and not f.my_pokemon.is_highest_level_in_party_ready_to_fight():
                        # switch to other pokemon
                        logger.info(f"Switch {f.my_pokemon} out of battle")
                        new_pk_index = OwnPokemon.party.get_index_of_highest_level_pokemon_ready_to_fight()
                        Selector.change_pokemon(new_pk_index) # perform the actual button clicks
                        f.my_pokemon = OwnPokemon.party[new_pk_index] # update the fight object
                    mode = 'max_damage' # now max damage the * out of this foe

                f.execute_best_move(mode=mode)
            elif sn == 'none_state':
                pass
            else:
                logger.debug(f"in a state I do not expect. Lets return")
                return
            sn = StateController.eval_state()
            logger.debug(f'State name {sn}')
            logger.debug(f"loop handle foe/ loop move")
        return f.next_foe_name # returns None if it has none


    @classmethod
    def handle_wild_and_trainer_fight(cls, wild=False,mode='max_damage'):
        from ..fundamentals import StateController
        # from fight.selector import Selector
        from ..fundamentals import btnA

        Selector.init_fight()

        # first lets check again
        StateController.eval_state()
        sn = StateController.state_name()
        while sn in ['fight_init', 'fight_init_trainer']: # if we keep hanging in the init state than keep initting
            Selector.init_fight()
            StateController.eval_state()
            sn = StateController.state_name()
        my_pokemon = [p for p in OwnPokemon.party if p.current_hp>0][0] # first pokemon with hp
        StateController.in_fight = True
        logger.debug(f'State name {StateController.state_name()}')
        while 'fight' in sn or 'none' in sn:  # loop over foe's
            next_foe_name = cls.handle_foe(my_pokemon, wild=wild, mode=mode)
            if next_foe_name is not None: # if there is a next pokemon chose options
                logger.debug("there is a next foe")
                cls.choose_new_pokemon('current_pokemon')
                logger.debug(f"Wait 1.5 sec for the new foe to appear")
                time.sleep(1.5)
            sn = StateController.state_name()
            if sn in ['fight_use_next_pokemon', 'fight_bring_out_which_pokemon']:
                logger.debug(f"My pokemon fainted but we use a next pokemon")
                if sn == 'fight_use_next_pokemon':
                    btnA()
                next_pokemon_idx = np.argmax([p.current_hp/p.stats['hp'] for p in OwnPokemon.party])
                logger.info(f"Next pokemon idx {next_pokemon_idx} with name {OwnPokemon.party[next_pokemon_idx]}")
                Selector.bring_out_or_choose_next_pokemon(next_pokemon_idx)
                my_pokemon = OwnPokemon.party[next_pokemon_idx]
            elif sn == 'fight_evolve':
                text = FightRec.read_bar()
                poke_name = Pokemon.get_closest_match_by_name(text.split('What')[1].split('isevol')[0])
                p = OwnPokemon.party.get_own_pokemon_by_own_name(poke_name)

                time.sleep(7)  # it takes time to evolve okeay..


                while 'into' not in text:
                    text = FightRec.read_bar()
                    logger.info('done yet?')
                    time.sleep(.5)

                text = FightRec.read_bar()
                new_name = text.split('into')[1]
                new_p = OwnPokemon.get_pokemon_by_name(Pokemon.get_closest_match_by_name(new_name))
                p.evolve(new_p)
                time.sleep(5)



            # else the battle has ended

            sn = StateController.eval_state()
            logger.debug(f'State name {StateController.state_name()}')

            logger.debug(f"New foe/my_pokemon loop")


    @classmethod
    def handle_fight(cls, mode='max_damage'):
        from ..fundamentals import StateController

        # first lets check again
        # StateController.eval_state()
        # sn = StateController.state_name()
        sn = 'fight'
        while 'fight' in sn or 'none' in sn:
            logger.debug(f'State name {StateController.state_name()}')
            if StateController.state_name() == 'fight_init_trainer':
                cls.handle_wild_and_trainer_fight(mode=mode)
            elif StateController.state_name() == 'fight_init':
                cls.handle_wild_and_trainer_fight(wild=True, mode=mode)
            else:
                cls.handle_wild_and_trainer_fight(mode=mode) # this is default
            logger.debug(f"new battle loop")
            StateController.eval_state()
            sn = StateController.state_name()


    # # ORIGINAL
    # @classmethod
    # def handle_fight(cls, mode = 'max_damage'):
    #     from fundamentals import StateController
    #     from fight.selector import Selector
    #     from fundamentals import btnA
    #
    #     # first lets check again
    #     StateController.eval_state()
    #     sn = StateController.state_name()
    #     while 'fight' in sn or 'none' in sn:
    #         StateController.eval_state()
    #         sn = StateController.state_name()
    #         print(f'State name {StateController.state_name()}')
    #         if StateController.state_name() == 'fight_init_trainer':
    #             Selector.init_fight()
    #         if StateController.state_name() == 'fight_init':
    #             Selector.init_fight()
    #         elif not ('f' in globals() or 'f' in locals()):
    #             # so the fight was not yet initiated
    #             f = Fight()
    #         elif StateController.state_name() == 'fight_pokedex':
    #             '''' A new pokemon was recently caught. Besides skipping the pokedex window we should add it to our
    #             party'''
    #
    #             print("handle pokedex state")
    #
    #             # maybe add the foe to the party or PC and leave out the needed info. make a state that checks if the
    #             # info of all pokemon present and if that is not the case it goes and checks it. This state is a
    #             # substate of the walk state as we can only check the states from the game menu (ony accessible when the
    #             # player is visible or in the walk state)
    #
    #             # ISSUE this should not be done in the pokedex state because if a pokemon is caught for the 2nd time the
    #             # pokedex will not pop up. So we need to create a obtain pokemon function which is called/ triggered by
    #             # the text in the bar. But it is always the end of the fight.
    #
    #             #f.foe.caught() # add foe to own pookemon
    #
    #             for i in range(3):
    #                 print("Bash B")
    #                 btnB()
    #                 time.sleep(1)
    #                 btnB()
    #             StateController.eval_state()
    #
    #         elif StateController.state_name() == 'fight_wait_arrow':
    #             text = FightRec.read_bar()
    #             # interpret text
    #             print(text)
    #             f.interpret_bar(tezxt)
    #             btnA()
    #             time.sleep(0.3)
    #         elif StateController.state_name() in ['fight_menu', 'fight_item', 'fight_pokemon','fight_move']:
    #             # we are in the main fight
    #             f.execute_best_move(mode=mode)
    #


if __name__ == '__main__':
    time.sleep(1)
    Selector.go_to_pokemon_stats_page_by_idx(1)

    # Fighter.eval_pokemon_stats()
    # test=1

