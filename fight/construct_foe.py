
import pytesseract
import re
import difflib
import os
from fundamentals.config import config
from fundamentals.screen import screen_grab, read_bar
from fundamentals.load_templates import load_templates
import numpy as np
import cv2
from pokemon import load_pokemon
from pokemon import SpecificPokemon

def create_foe():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    path = config('../settings.ini', 'tesseract','path')
    w = int(config('../settings.ini', 'window_size', 'native_w'))
    h = int(config('../settings.ini', 'window_size', 'native_h'))
    pytesseract.pytesseract.tesseract_cmd = path

    screen = screen_grab(resize=True)
    screen_large = screen_grab()
    roi_foe_name = screen[0:int(8 * w / 144), 0:int(100 * h / 160)]  # roi screen shot size roi = screen[0:9, 0:100]

    # add a white part above above and below the name. This makes it easier for tesseract to read.
    h1, w1 = roi_foe_name.shape
    white = 248 * np.ones((10, w1), dtype=np.uint8)
    img_foe_name = cv2.vconcat([white, roi_foe_name, white])

    # read the text in the name area
    text_foe_name = pytesseract.image_to_string(img_foe_name, lang='Pokemon').lower()

    # check which pokemon_name resembles the read name best
    if 'df_pokemon' not in globals():
        df_pokemon = load_pokemon()

    foe_name = difflib.get_close_matches(text_foe_name, list(df_pokemon['pokemon_name']) , n=1)[0]

    print('Foe name is ' + foe_name)

    roi_foe_level = screen_large[int(8 * h * 4 / 144):int(18 * h * 4/ 144),
                    int(40 * w * 4 / 160):int(60 * w * 4 / 160)]  # roi screen shot size roi = screen[0:9, 0:100]
    # add a white part above, below, right and left the name. This makes it easier for tesseract to read.
    h1, w1 = roi_foe_level.shape
    white = 248 * np.ones((h1,10), dtype=np.uint8)
    img_foe_level = cv2.hconcat([white, roi_foe_level, white])
    white = 248 * np.ones((10, w1+20), dtype=np.uint8)
    img_foe_level = cv2.vconcat([white, img_foe_level, white])


    text_foe_level = pytesseract.image_to_string(img_foe_level, lang='Pokemon')
    print(text_foe_level)

    ##test
    # cv2.imshow('level', img_foe_level)
    # cv2.waitKey()

#TODO so tesseract does not recognize just the digits it appears. It also needs the :L in the image
# Fix this with documentation so we just read the digits. In that case part below can be dropped

    # foe_level = 1
    # flp = re.split(':1.', text_foe_level)  # 1.
    # if len(flp) == 1:
    #     flp = re.split(':1', flp[0])  # 1
    #     print(flp)
    # if len(flp) == 1:
    #     flp = re.split(':l.', flp[0])  # L.
    #     print(flp)
    # # print(len(flp))
    # if len(flp) == 1:
    #     flp = re.split(':l', flp[0])  # L
    #     # print(flp)
    # if flp[1].isdigit():
    #     flp = int(flp[1])
    #     if flp < 100 and flp > 0:
    #         foe_level = flp

    #print('Foe level is ' + str(foe_level))
    # Retreive foe data

    id = df_pokemon[df_pokemon['pokemon_name'] == foe_name]['pokemon_id']
    type1 = df_pokemon[df_pokemon['pokemon_name'] == foe_name]['type1']
    type2 = df_pokemon[df_pokemon['pokemon_name'] == foe_name]['type2']
    hp = df_pokemon[df_pokemon['pokemon_name'] == foe_name]['hp']

    # just hp for testing
    foe = SpecificPokemon(id, foe_name, type1, type2, {'hp':hp}, int(foe_level))


    # foe_types = ['', '']
    # for n in range(len(poke_name_list)):
    #     if foe_name_lst[0] == poke_name_list[n]:
    #         foe_types[0] = sheet.cell(n + 1, 11).value
    #         foe_types[1] = sheet.cell(n + 1, 12).value
    #         foe_def = sheet.cell(n + 1, 6).value
    #         foe_spd = sheet.cell(n + 1, 8).value
    # foe_info = [foe_types, foe_level, foe_def, foe_spd]
    # return foe_info

if __name__ == '__main__':
    load_pokemon()
    create_foe()
    a=1