
# from main import go_to, train, buy, talk


class Gameplan:

    continue_or_new_game = 'new_game'

    # game setup
    # player_name = 'automation'
    # foe_name = 'manual'

    player_name = 'blue'
    rival_name = 'red'

    starter_pokemon = 'charmander' # choose charmander/squirtle/bulbasor of zoiets
    catch_pokemon = ['pidgey', 'pikachu', 'geodude']

    sku = {'item_name': 'Poke Ball', 'amount': 10}

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

    # to_level, which_pokemon, start, turn, heal_point,

    plan = [{'function': 'go',      'args': ('route1', 595)},
            {'function': 'talk',    'args': _starter_pokemon_location[starter_pokemon]},
            {'function': 'talk',    'args': _mom},
            {'talk': 'talk',        'args': viridian_city_pc},  # poke center in viridian city
            {'talk': viridian_city_market},  # pick up the parcel
            # {'talk': _oak},  # deliver parcel to oak
            # {'talk': _mom},
            # {'talk': pc},  # return to viridian city
            # {'go': ('pewter_city', 754)},  # go to pewter city though viridian forest
            # {'talk': pc},
            # {'train': _train_pewter},
            # {'talk': ('pewter_city_gym', 20)}  # engage in fight with brock
            ]

    # plan = [(go_to,     (('route1', 595))),
    #         (talk,      (_starter_pokemon_location[starter_pokemon])),
    #         (talk,      (_mom)),
    #         (talk,      (viridian_city_pc)),
    #         (talk,      (viridian_city_market)), # get parcel
    #         (talk,      (_oak)), # deliver parcel to oak
    #         (talk,      (viridian_city_pc)),
    #         (buy,       (viridian_city_market, 'Poke Ball', 5)),
    #         (talk,      (pewter_city_pc)),
    #         (train,     (10, 'all', ('route2b', 68), ('route2b', 61), pewter_city_pc ))
    #         ]


    @classmethod
    def exceute(cls):
        [f(*args) for f, args in cls.plan]


if __name__ == '__main__':
    Gameplan.exceute()


