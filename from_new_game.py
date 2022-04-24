
# from pokebot.fundamentals.initialization import get_custom_logger

import logging
from datetime import datetime

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
                        handlers=[logging.FileHandler(f"log\\{datetime.utcnow().strftime('%Y-%m-%dT%H_%M_%S')}.log"),
                                  logging.StreamHandler()])
logging.info('test')
from pokebot import Gameplan, train, talk, buy, go_to, catch, open_vba
import pokebot.short_cuts as sc


Gameplan.continue_or_new_game = 'new_game'
Gameplan.starter_pokemon = 'squirtle'
Gameplan.player_name = 'blue'
Gameplan.catch_pokemon = ['pidgey', 'pikachu', 'geodude','nidoran_f']

go_to(('route1', 595))
talk(sc.starter_pokemon_location[Gameplan.starter_pokemon])
talk(sc.mom)
talk(sc.viridian_city_pc)
talk(sc.viridian_city_market)
talk(sc.oak)
talk(sc.mom)
talk(sc.viridian_city_pc)
buy(sc.viridian_city_market, 'poke ball', 9)
catch('pidgey', ('route1', 168), ('route1', 161), sc.viridian_city_pc)
train(5, 'all', ('route1', 168), ('route1', 161), sc.viridian_city_pc)
talk(sc.viridian_city_pc)
talk(sc.pewter_city_pc)
train(10, Gameplan.starter_pokemon,  ('route2b', 68), ('route2b', 61), sc.pewter_city_pc)
talk(sc.pewter_city_pc)
go_to(('pewter_city_gym', 55))
talk(sc.pewter_city_pc)
talk(sc.brock)
go_to(sc.pewter_city_pc)




# class Legacy:

#     plan = [
#         (go_to, [('route1', 595)]),
#         (talk, [starter_pokemon_location[starter_pokemon]]),
#         (talk, [mom]),
#         (talk, [viridian_city_pc]),
#         (talk, [viridian_city_market]),  # get parcel
#         (talk, [oak]),  # deliver parcel to oak
#         (talk, [mom]),
#         (talk, [viridian_city_pc]),
#         (buy, [viridian_city_market, 'poke ball', 9]),
#
#         (catch, ['pidgey', ('route1', 168), ('route1', 161), viridian_city_pc]),
#         (train, [5, 'all', ('route1', 168), ('route1', 161), viridian_city_pc]),
#         (talk, [pewter_city_pc]),
#         (train, [6, 'all', ('route2b', 68), ('route2b', 61), pewter_city_pc]),
#         (talk, [pewter_city_pc]),
#         (go_to, [('pewter_city_gym', 55)]),  # challenge the only trainer it brock's gym
#         (talk, [pewter_city_pc]),
#         (talk, [brock]),  # fight brock
#         (talk, [pewter_city_pc]),
#
#     ]
#
#     @classmethod
#     def exceute(cls):
#         [f(*args) for f, args in cls.plan]

#     starter_pokemon = 'squirtle'  # choose charmander/squirtle/bulbasor of zoiets
#
#     sku = {'item_name': 'poke ball', 'amount': 10}
#
#     # location aliases
#     mom = ('mom_lvl1', 38, 'up')
#     oak = ('oaks_lab', 26, 'up')
#     brock = ('pewter_city_gym', 15, 'up')
#     viridian_city_pc = ('viridian_city_pc', 4, 'up')
#     pewter_city_pc = ('pewter_city_pc', 4, 'up')
#     viridian_city_market = ('viridian_city_market', 27, 'left')
#
#     starter_pokemon_location = {'charmander': ('oaks_lab', 37, 'up'),
#                                  'squirtle': ('oaks_lab', 38, 'up'),
#                                  'bulbasaur': ('oaks_lab', 39, 'up')}
#
#     # train viridian
#     train_viridian = {'to_level': 7,
#                        'pokemon': 'all',
#                        'start': ('route1', 161),
#                        'turn': ('route1', 168)}
#     train_pewter = {'to_level': 10,
#                      'pokemon': 'all',
#                      'start': ('route2b', 26),
#                      'turn': ('route2b', 68)}
#