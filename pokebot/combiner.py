from .walk import Walker, Position, LocationNotFound, WrongStep
from .fundamentals import StateController, btnA
from .fight import Fighter
from .gameplay.gameplay import Gameplay
import time

def go_to(goal, fight_mode='max_damage'):
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
                time.sleep(1)  # take some time before the full text appears
                Walker.handle_talk()
                time.sleep(0.1)
            elif 'gameplay' in sn:
                Gameplay.handle_gameplay()
            print(f"LOOP GO_TO. current {Position.map_name} {Position.cor_id} ")
        print("END")

    except Walker.GameplayException as e:
        print(e)


def talk(goal, fight_mode='max_damage'):
    go_to(goal, fight_mode=fight_mode)
    # TAKE CASE OF ORIENTATION FIRST
    sn = StateController.eval_state()
    while sn != 'walk_talk':
        btnA(1)  # check is talk state is reached
        print("Pressing A to start monologue")
        sn = StateController.eval_state()
        print(f"In talk main function sn: {sn}")
    Walker.handle_talk()


def buy(goal, item_name, amount):
    from .gameplay import Gameplay
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


def catch(pokemon_name, start, turn, heal_point, hp_limit=0.3):
    from .fight import OwnPokemon
    from pokebot.game_plan import Gameplan

    if pokemon_name not in Gameplan.catch_pokemon:
        raise Exception(f"Pokemon {pokemon_name} not in the catch list of Gameplan.catch_pokemon")

    hp_fractions = sum([p.current_hp / p.stats['hp'] for p in OwnPokemon.party]) / len(OwnPokemon.party)
    while pokemon_name not in [p.name for p in OwnPokemon.party]:  # empty list is False
        # train
        while pokemon_name not in [p.name for p in OwnPokemon.party] and hp_fractions >= hp_limit:
            print(f"Party: {OwnPokemon.party}")

            go_to(start, fight_mode='train')
            go_to(turn, fight_mode='train')

            hp_fractions = sum([p.current_hp / p.stats['hp'] for p in OwnPokemon.party]) / len(OwnPokemon.party)

        while pokemon_name not in [p.name for p in OwnPokemon.party] and hp_fractions < hp_limit:
            print(f"Party: {OwnPokemon.party}")
            talk(heal_point, fight_mode='train')
            OwnPokemon.party.heal_party()

            hp_fractions = sum([p.current_hp / p.stats['hp'] for p in OwnPokemon.party]) / len(OwnPokemon.party)


def train(to_level, which_pokemon, start, turn, heal_point, hp_limit=0.3):
    '''' this function trains pokemon to a certain level

     to_level: int                              to which level to train
     which_pokemon: str                         the name of the pokemon, or maybe index
     start: (map, cor_id)                       the coordinate of the start
     trun: (map, cor_id)                        the coordinate of the turn
     heal_point: (map, cor_id, orientation)     the point to heal so a talk can be started
     heal_limit: float                          the average percentage of health of all being trained pokemon
     '''

    from .fight import OwnPokemon

    if which_pokemon == 'all':
        '''' first make a list of all pokemon in party that need training
         then make a list of all pokemon that have hp>0 and need training
         while both are true we fight. if no pokemon ready to fight we go 
         to pc.'''
        pokemon_to_train = [p for p in OwnPokemon.party if p.level < to_level]
        pokemon_to_train_ready_to_fight = [p for p in pokemon_to_train if p.current_hp > 0]
        hp_fractions = sum([p.current_hp / p.stats['hp'] for p in OwnPokemon.party]) / len(OwnPokemon.party)

        while pokemon_to_train:  # empty list is False
            # train
            while pokemon_to_train and (pokemon_to_train_ready_to_fight and hp_fractions >= hp_limit):
                print(f"Party: {OwnPokemon.party}")
                print(f"to train and ready to fight: {pokemon_to_train_ready_to_fight}")
                Fighter.put_pokemon_in_front_of_party(pokemon_to_train_ready_to_fight[0])

                go_to(start, fight_mode='train')
                go_to(turn, fight_mode='train')

                pokemon_to_train = [p for p in OwnPokemon.party if p.level < to_level]
                pokemon_to_train_ready_to_fight = [p for p in pokemon_to_train if
                                                   p.current_hp > 0]  # could be [] so we put [0] at the first row of thies loop
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
