from walker import Walker
#from walk.position import
from fundamentals.state_controller import StateController
from fight import Fighter
from stepper import WrongStep
from position import LocationNotFound
from gameplay.gameplay import Gameplay
import time

def go_to(goal):
    while not (Walker.map_name == goal[0] and Walker.cor_id == goal[1]):
        StateController.eval_state()
        sn = StateController.state_name()  # state name
        print(f"sn in mMain LOOP : {sn}")
        if sn == 'walk':
            try:
                Walker.go(goal)
            except (WrongStep, LocationNotFound) as e:
                print(F'ERROR: {e}')
        elif 'fight' in sn:  # or  'none' in sn:  ## removed this part
            Fighter.handle_fight(mode='max_damage')  # catch or max_damage
        elif sn == 'walk_evalstats':
            Fighter.eval_pokemon_stats()
        elif sn == 'walk_talk':
            time.sleep(1) # take some time before the full text appears
            Walker.handle_talk()
        elif 'gameplay' in sn:
            Gameplay.handle_gameplay()

        print(f"LOOP GO_TO. current {Walker.map_name} {Walker.cor_id} ")
    print("END")

def talk(goal):
    from fundamentals.controls import btnA
    go_to(goal)
    # TAKE CASE OF ORIENTATION FIRST
    sn = StateController.eval_state()
    while sn != 'walk_talk':
        btnA(1) # check is talk state is reached
        print("Pressing A to start monologue")
        sn = StateController.eval_state()
    Walker.handle_talk()


def buy(goal, item_name, amount):
    from fundamentals.controls import btnA
    from gameplay.gameplay import Gameplay
    StateController.eval_state()
    sn = StateController.state_name()
    while sn != 'walk_market':
        talk(goal)
        StateController.eval_state()
        sn = StateController.state_name()
    while sn != 'gameplay_buy_menu':
        btnA()
        StateController.eval_state()
        sn = StateController.state_name()
    Gameplay.buy_item(item_name, amount)


def train(to_level, which_pokemon, start, turn):
    from fight.pokemon import OwnPokemon

    if which_pokemon == 'all':
        min_level = min([p.level for p in OwnPokemon.party])
        hp_fractions = sum([p.current_hp / p.stats['hp'] for p in OwnPokemon.party]) / len(OwnPokemon.party)
        while min_level < to_level:
            # train
            while (hp_fractions > 0.3) and (min_level < to_level):
                go_to(start)
                go_to(turn)
                min_level = min([p.level for p in OwnPokemon.party])
                hp_fractions = sum([p.current_hp / p.stats['hp'] for p in OwnPokemon.party]) / len(OwnPokemon.party)
                print(f"MIN level: {min_level}")
            while hp_fractions <= 0.3:
                talk(('pc', 4, 'up'))
                OwnPokemon.party.heal()
                min_level = min([p.level for p in OwnPokemon.party])
                hp_fractions = sum([p.current_hp / p.stats['hp'] for p in OwnPokemon.party]) / len(OwnPokemon.party)



if __name__ == '__main__':
    #talk(('route2a_ptb_viridian_forest', 38, 'right'))



    # open_vba()



    # go_to('viridian_forest', 1)
    # go_to('mom_lvl1', 3)
    # go_to('route2a', 1)

    # train(9, 'all', ('route1', 161), ('route1', 168))


    from game_plan import Gameplan

    for step in Gameplan.plan:
        if step['function'] == 'go':
            go_to(step['args'])
        elif step['function'] == 'talk':
            talk(step['args'])
        elif step['function'] == 'train':
            train(*step['args'])
        elif step['function'] == 'buy':
            buy(*step['args'])



