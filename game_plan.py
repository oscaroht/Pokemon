



class Gameplan:

    continue_or_new_game = 'new_game'

    # game setup
    # player_name = 'automation'
    # foe_name = 'manual'

    player_name = 'blue'
    rival_name = 'red'

    starter_pokemon = 'charmander' # choose charmander/squirtle/bulbasor of zoiets
    catch_pokemon = ['pidgey', 'pikachu', 'geodude', 'caterpie', 'rattata']

    sku = {'item_name': 'Poke Ball', 'amount': 10}


    # location aliases
    _mom = ('mom_lvl1', 38, 'up')
    _oak = ('oaks_lab', 26, 'up')
    pc = ('pc', 4, 'up')
    market = ('market', 27, 'left')

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

    plan = [#{'function': 'go',      'args': ('route1', 595)},
            {'function': 'talk',    'args': _starter_pokemon_location[starter_pokemon]},
            {'function': 'talk',    'args': _mom},
            # {'talk': pc},  # poke center in viridian city
            # {'talk': market},  # pick up the parcel
            # {'talk': _oak},  # deliver parcel to oak
            # {'talk': _mom},
            # {'talk': pc},  # return to viridian city
            # {'go': ('pewter_city', 754)},  # go to pewter city though viridian forest
            # {'talk': pc},
            # {'train': _train_pewter},
            # {'talk': ('pewter_city_gym', 20)}  # engage in fight with brock
            ]

    # pyplan=[]
    # for step in plan:
    #     x
    #     pyplan.append({'function': step.keys()})
    #
    # pyplan =