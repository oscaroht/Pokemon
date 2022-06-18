
# from pokebot.fundamentals.initialization import get_custom_logger

import logging
from datetime import datetime
from pokebot.gameplay.item import Items

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
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
catch('pikachu', ('viridian_forest', 193), ('viridian_forest', 737), sc.pewter_city_pc)
train(7, 'all',  ('route2b', 68), ('route2b', 61), sc.pewter_city_pc)
train(12, Gameplan.starter_pokemon,  ('route2b', 68), ('route2b', 61), sc.pewter_city_pc)
talk(sc.pewter_city_pc)
go_to(('pewter_city_gym', 55))
talk(sc.pewter_city_pc)
while not Items.do_i_have('bolder badge'):
    talk(sc.brock)  # talk cannot be alone in a while loop
    go_to(('pewter_city_gym', 125))
talk(sc.pewter_city_pc)  # heal after successful gym battle
talk(sc.route3b_pc)
train(10, 'all',  ('route3b', 359), ('route3b', 364), sc.route3b_pc)
talk(sc.route3b_pc)
talk(sc.helix_fossil)
talk(sc.cerulean_city_pc)
train(13, 'all',  ('route4', 902), ('route4', 893), sc.cerulean_city_pc)
talk(sc.cerulean_city_pc)
go_to(('route24', 427))  # battle rival
talk(sc.cerulean_city_pc)
talk(('bill', 30, 'right'))  # take to pokemon bill
talk(('bill', 26, 'up'))  # start bill's computer
talk(('bill', 29, 'up'))  # take to human bill
talk(sc.cerulean_city_pc)
go_to(('cerulean_city_gym', 10))  # beat all trainers in cerulean gym
talk(sc.cerulean_city_pc)
while not Items.do_i_have('cascade badge'):
    talk(('cerulean_city_gym', 4, 'left'))  # talk cannot be alone in a while loop
    go_to(('cerulean_city_gym', 69))
talk(sc.cerulean_city_pc)
