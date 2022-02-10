from walker import Walker
#from walk.position import
from fundamentals.state_controller import StateController
from fight import Fighter
from stepper import WrongStep
from position import LocationNotFound
from gameplay.gameplay import Gameplay
import time
from fundamentals.controls import *
import numpy as np





def go_to(goal, fight_mode = 'max_damage'):

    try:
        while not Walker.reached_goal(goal):
            sn = StateController.eval_state()
            print(f"sn in mMain LOOP : {sn}")
            if sn == 'walk':
                try:
                    Walker.go(goal)
                except (WrongStep, LocationNotFound) as e:
                    print(F'ERROR: {e}')
            elif 'fight' in sn:  # or  'none' in sn:  ## removed this part
                Fighter.handle_fight(mode=fight_mode)  # catch or max_damage
            elif sn == 'walk_evalstats':
                Fighter.eval_pokemon_stats()
            elif sn == 'walk_talk':
                time.sleep(1) # take some time before the full text appears
                Walker.handle_talk()
                time.sleep(0.1)
            elif 'gameplay' in sn:
                Gameplay.handle_gameplay()
            print(f"LOOP GO_TO. current {Walker.map_name} {Walker.cor_id} ")
        print("END")

    except Walker.GameplayException as e:
        print(e)



def talk(goal, fight_mode = 'max_damage'):
    from fundamentals.controls import btnA
    go_to(goal, fight_mode=fight_mode)
    # TAKE CASE OF ORIENTATION FIRST
    sn = StateController.eval_state()
    while sn != 'walk_talk':
        btnA(1) # check is talk state is reached
        print("Pressing A to start monologue")
        sn = StateController.eval_state()
        print(f"In talk main function sn: {sn}")
    Walker.handle_talk()


def buy(goal, item_name, amount):
    from fundamentals.controls import btnA
    from gameplay.gameplay import Gameplay
    StateController.eval_state()
    sn = StateController.state_name()
    while sn != 'walk_market' or 'buy' in sn:
        if 'buy' in sn:
            break
        go_to(goal)
        print("Pressing A to start market menu")
        btnA(1)  # start talking
        StateController.eval_state()
        sn = StateController.state_name()
    # while sn != 'gameplay_buy_menu':
    #     btnA()
    #     StateController.eval_state()
    #     sn = StateController.state_name()
    Gameplay.buy_item(item_name, amount)


def train(to_level, which_pokemon, start, turn, heal_point, hp_limit=0.3):
    '''' this function trains pokemon to a certain level

     to_level: int                              to which level to train
     which_pokemon: str                         the name of the pokemon, or maybe index
     start: (map, cor_id)                       the coordinate of the start
     trun: (map, cor_id)                        the coordinate of the turn
     heal_point: (map, cor_id, orientation)     the point to heal so a talk can be started
     heal_limit: float                          the average percentage of health of all being trained pokemon
     '''

    from fight.pokemon import OwnPokemon

    if which_pokemon == 'all':
        '''' first make a list of all pokemon in party that need training
         then make a list of all pokemon that have hp>0 and need training
         while both are true we fight. if no pokemon ready to fight we go 
         to pc.'''
        pokemon_to_train = [p for p in OwnPokemon.party if p.level < to_level]
        pokemon_to_train_ready_to_fight = [p for p in pokemon_to_train if p.current_hp>0]
        hp_fractions = sum([p.current_hp / p.stats['hp'] for p in OwnPokemon.party]) / len(OwnPokemon.party)

        while pokemon_to_train: # empty list is False
            # train
            while pokemon_to_train and (pokemon_to_train_ready_to_fight and hp_fractions >= hp_limit):
                print(f"Party: {OwnPokemon.party}")
                print(f"to train and ready to fight: {pokemon_to_train_ready_to_fight}")
                Fighter.put_pokemon_in_front_of_party(pokemon_to_train_ready_to_fight[0])

                go_to(start, fight_mode='train')
                go_to(turn, fight_mode='train')

                pokemon_to_train = [p for p in OwnPokemon.party if p.level < to_level]
                pokemon_to_train_ready_to_fight = [p for p in pokemon_to_train if p.current_hp > 0] # could be [] so we put [0] at the first row of thies loop
                print(f'Pokemon to train: {[p.own_name for p in pokemon_to_train_ready_to_fight]}')
                hp_fractions = sum([p.current_hp / p.stats['hp'] for p in OwnPokemon.party]) / len(OwnPokemon.party)

            while pokemon_to_train and (not pokemon_to_train_ready_to_fight or hp_fractions < hp_limit):
                print(f"Party: {OwnPokemon.party}")
                print(f"to train and ready to fight: {pokemon_to_train_ready_to_fight}")
                talk(heal_point, fight_mode='train')
                OwnPokemon.party.heal_party()

                pokemon_to_train = [p for p in OwnPokemon.party if p.level < to_level]
                pokemon_to_train_ready_to_fight = [p for p in pokemon_to_train if p.current_hp > 0]
                print(f'Pokemon to train: {[p.own_name for p in pokemon_to_train_ready_to_fight]}')
                hp_fractions = sum([p.current_hp / p.stats['hp'] for p in OwnPokemon.party]) / len(OwnPokemon.party)



class Gameplan2:


    starter_pokemon = 'charmander' # choose charmander/squirtle/bulbasor of zoiets

    sku = {'item_name': 'poke ball', 'amount': 10}

    # location aliases
    _mom = ('mom_lvl1', 38, 'up')
    _oak = ('oaks_lab', 26, 'up')
    brock = ('pewter_city_gym', 15, 'up')
    viridian_city_pc = ('viridian_city_pc', 4, 'up')
    pewter_city_pc = ('pewter_city_pc', 4, 'up')
    viridian_city_market = ('viridian_city_market', 27, 'left')

    _starter_pokemon_location = {'charmander': ('oaks_lab', 37, 'up'),
                                'squirtle': ('oaks_lab', 38, 'up'),
                                'bulbasaur': ('oaks_lab', 39, 'up')}

    #train viridian
    _train_viridian = {'to_level': 7,
                       'pokemon': 'all',
                       'start': ('route1', 161),
                       'turn': ('route1', 168)}
    _train_pewter = {'to_level': 10,
                       'pokemon': 'all',
                       'start': ('route2b', 26),
                       'turn': ('route2b', 68)}

    plan = [
            # (go_to,     [('route1', 595)]),
            # (talk,      [_starter_pokemon_location[starter_pokemon]]),
            # (talk,      [_mom]),
            # (talk,      [viridian_city_pc]),
            # (talk,      [viridian_city_market]), # get parcel
            # (talk,      [_oak]), # deliver parcel to oak
            # (talk,      [_mom]),
            # (talk,      [viridian_city_pc]),
            # (buy,       [viridian_city_market, 'poke ball', 9]),

            (go_to,     [('route1', 168)]),

            (train,     [5, 'all', ('route1', 168), ('route1', 161), viridian_city_pc]),
            (talk,      [pewter_city_pc]),
            (talk,      [viridian_city_pc]),
            (talk,      [pewter_city_pc]),
            (train,     [7, 'all', ('route2b', 68), ('route2b', 61), pewter_city_pc]),
            (go_to,     [('pewter_city_gym', 55)]),
            (talk,      [pewter_city_pc]),
            (talk,      [brock]), # fight brock
            (talk,      [pewter_city_pc]),

            ]


    @classmethod
    def exceute(cls):
        [f(*args) for f, args in cls.plan]

if __name__ == '__main__':
    Gameplan2.exceute()

    # talk((Gameplan.viridian_city_market))

    # buy(('viridian_city_market', 27, 'left'), 'poke ball', 2)

    # go_to(('pewter_city_pc', 42, 'up'))
    # Walker.map_name = 'viridian_city'
    # talk(('viridian_city_pc', 4, 'up'))


    # def testaa():
    #     # keyboard.press('d')
    #     time.sleep(0.03500)
    #     # keyboard.release('d')
    #     time.sleep(0.4)
    #
    # from timeit import Timer
    # for i in range(20):
    #     # t = Timer(lambda: testaa())
    #     # print(t.timeit(number=1))
    #     start = time.time()
    #     testaa()
    #     print(time.time()-start)

    # train(9,'all', ('route1', 161), ('route1', 168), ('viridian_city_pc', 4, 'up'))

    #talk(('route2a_ptb_viridian_forest', 38, 'right'))

    # open_vba()

    # go_to('viridian_forest', 1)
    # go_to('mom_lvl1', 3)
    # go_to('route2a', 1)

    # train(9, 'all', ('route1', 161), ('route1', 168))

    # plan = {train:((1,2), 3)}
    # [f(*args) for f, args in plan.items() ]
    #
    # from game_plan import Gameplan
    #
    # for step in Gameplan.plan:
    #     if step['function'] == 'go':
    #         go_to(step['args'])
    #     elif step['function'] == 'talk':
    #         talk(*step['args'])
    #     elif step['function'] == 'train':
    #         train(*step['args'])
    #     elif step['function'] == 'buy':
    #         buy(*step['args'])



