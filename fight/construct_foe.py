
import pytesseract
import re
import difflib
import os
from fundamentals.config import config
from fundamentals.screen import screen_grab, read_bar
from fundamentals.load_templates import load_templates
import numpy as np
import cv2
from pokemon import party, own_pokemon, df_pokemon, df_moves, df_strength_weakness
from pokemon import WildPokemon

def create_foe():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    path = config('../settings.ini', 'tesseract','path')
    w = int(config('../settings.ini', 'window_size', 'native_w'))
    h = int(config('../settings.ini', 'window_size', 'native_h'))
    pytesseract.pytesseract.tesseract_cmd = path

    screen = screen_grab(resize=True)
    screen_large = screen_grab()
    roi_foe_name = screen[0:int(8 * w / 144), 0:int(100 * h / 160)]  # roi screen shot size roi = screen[0:9, 0:100]

    """" Get name """
    # add a white part above above and below the name. This makes it easier for tesseract to read.
    h1, w1 = roi_foe_name.shape
    white = 248 * np.ones((10, w1), dtype=np.uint8)
    img_foe_name = cv2.vconcat([white, roi_foe_name, white])

    ## test
    # cv2.imshow('name', img_foe_name)
    # cv2.waitKey()

    # read the text in the name area
    text_foe_name = pytesseract.image_to_string(img_foe_name,lang='eng', config='-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ').lower()

    # check which pokemon_name resembles the read name best
    foe_name = difflib.get_close_matches(text_foe_name, list(df_pokemon['pokemon_name']) , n=1)[0]
    print('Foe name is ' + foe_name)


    """" Get level """
    roi_foe_level = screen_large[int(8 * h * 4 / 144):int(18 * h * 4/ 144),
                    int(40 * w * 4 / 160):int(60 * w * 4 / 160)]  # roi screen shot size roi = screen[0:9, 0:100]

    ## test
    # cv2.imshow('level', roi_foe_level)
    # cv2.waitKey()

    """" page segmentation mode psm 13 is raw text, psm 8 (one word could also be used. The oem does not appear to matter much """
    foe_level = pytesseract.image_to_string(roi_foe_level, lang='Pokemon', config='--oem 0 -c tessedit_char_whitelist=1234567890 --psm 13')

    foe_series = df_pokemon[df_pokemon['pokemon_name'] == foe_name ]
    foe = WildPokemon(foe_series.index[0],
                      foe_series.iloc[0]['pokemon_name'],
                      foe_series.iloc[0]['type1'],
                      foe_series.iloc[0]['type2'],
                      {'hp':foe_series.iloc[0]['base_hp'],
                            'atk':foe_series.iloc[0]['base_atk'],
                            'def':foe_series.iloc[0]['base_def'],
                            'spa':foe_series.iloc[0]['base_spa'],
                            'spd':foe_series.iloc[0]['base_spa'],
                            'spe':foe_series.iloc[0]['base_spe'] } ,
                      int(foe_level) )
    return foe


def calculate_damage(my_pokemon, move ,foe ):

    if move.id == -1:
        return 0

    special_moves=['water','grass','fire','ice','electric','psychic']
    physical_moves=['normal','fighting','flying','ground','rock','bug','ghost','poison']

    if move.type == my_pokemon.type1 or move.type == my_pokemon.type2:
        stab = 1.5
    else:
        stab = 1

    multiplier = df_strength_weakness[ (df_strength_weakness['atk'] == move.type) & (df_strength_weakness['def'] == foe.type1)  ].iloc[0]['multiplier'] # has to be iloc instead of loc because we are not using the indexes
    if foe.type2 != '-':
        multiplier_2 = df_strength_weakness[ (df_strength_weakness['atk'] == move.type) & (df_strength_weakness['def'] == foe.type2) ].iloc[0]['multiplier'] # has to be iloc instead of loc because we are not using the indexes
        multiplier *= multiplier_2
    random = 235.5/254 # this is a normally distributed range between 217 and 254

    modifier = random * multiplier * stab

    critical = 1 # if it is a critical hit this should be 2

    """" from https://bulbapedia.bulbagarden.net/wiki/Damage#Damage_calculation
     the 100/50 gives special moves such as growl also damage. Which should not be the case."""
    if move.type in special_moves:
        damage = ( ((2/5)*my_pokemon.level*critical+2) * move.power * my_pokemon.stats['spa']/foe.stats['spd'] +100 )/50 * modifier
    elif move.type in physical_moves:
        damage = ( ((2/5)*my_pokemon.level*critical+2) * move.power * my_pokemon.stats['atk']/foe.stats['def'] +100 )/50 * modifier
    else:
        raise Exception(f'Move type {move.type} unknown.')

    return damage

def calculate_best_move(my_pokemon, foe):
    d = []
    for i in range(4):
        if my_pokemon.moves[i].id != -1 and my_pokemon.moves[i].pp > 0:     # nice conditionals are checked one at a time
            d += [ calculate_damage(my_pokemon, my_pokemon.moves[i], foe) ]

    # d2 = calculate_damage(my_pokemon, my_pokemon.move2, foe)
    # d3 = calculate_damage(my_pokemon, my_pokemon.move3, foe)
    # d4 = calculate_damage(my_pokemon, my_pokemon.move4, foe)
    return np.argmax(d) # so argmax 0 becomes move 1


if __name__ == '__main__':
    my_pokemon = own_pokemon[0]
    foe = create_foe()

    best_move_idx = calculate_best_move(my_pokemon,foe)

    test=1


