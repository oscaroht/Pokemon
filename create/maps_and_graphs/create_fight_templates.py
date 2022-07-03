import numpy as np
import cv2


def fight_menu():
    img = cv2.imread('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\menu\\fight_menu.png')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = np.zeros(img.shape[:2], dtype="uint8")
    cv2.rectangle(mask, (80, 90), (160, 144), 255, -1)
    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\menu\\fight_menu_mask.png', mask)

def moves():
    img = cv2.imread('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\move\\fight_move.png')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = np.zeros(img.shape[:2], dtype="uint8")
    cv2.rectangle(mask, (0, 137), (160, 144), 255, -1)
    cv2.rectangle(mask, (0, 60), (6, 144), 255, -1)
    cv2.rectangle(mask, (0, 95), (40, 144), 255, -1)
    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\move\\fight_move_mask.png', mask)

def battle_menu():
    img = cv2.imread('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\selector\\menu\\move_menu.png')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = np.zeros(img.shape[:2], dtype="uint8")
    cv2.rectangle(mask, (65, 90), (160, 144), 255, -1)

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\selector\\menu\\move_menu_mask.png', mask)

def move_selector():
    img = cv2.imread('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\move\\1\\1.png')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = np.zeros(img.shape[:2], dtype="uint8")
    cv2.rectangle(mask, (40, 100), (46, 137), 254, -1)

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\move\\1\\1_mask.png', mask)

def wait_arrow():
    img = cv2.imread('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\wait_arrow\\wait_arrow.png')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = np.zeros(img.shape[:2], dtype="uint8")
    cv2.rectangle(mask, (143, 127), (151, 136), 255, -1)

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\wait_arrow\\wait_arrow_mask.png', mask)

def fight_init1():
    img = cv2.imread('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\init\\init.png')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = np.ones(img.shape[:2], dtype="uint8")
    cv2.rectangle(mask, (0, 0), (145, 87), 0, -1)  # (x0,y0), (x1,y1)
    cv2.rectangle(mask, (0, 0), (100, 35), 225, -1)
    cv2.rectangle(mask, (0, 88), (65, 95), 0, -1)
    cv2.rectangle(mask, (8, 103), (150, 135), 0, -1)  # hides the bar

    # cv2.rectangle(mask, (0, 95), (40, 144), 255, -1)

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\init\\init_mask.png', mask)

def fight_init2():
    img = cv2.imread('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\init\\init.png')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = np.ones(img.shape[:2], dtype="uint8")
    cv2.rectangle(mask, (0, 0), (145, 87), 0, -1)  # (x0,y0), (x1,y1)
    cv2.rectangle(mask, (0, 0), (80, 100), 225, -1)
    cv2.rectangle(mask, (8, 103), (150, 135), 0, -1)  # hides the bar

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\init\\init_mask.png', mask)



def pass_mask():
    img = cv2.imread('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\pass\\pass.png')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = np.ones(img.shape[:2], dtype="uint8")
    cv2.rectangle(mask, (0, 0), (145, 87), 0, -1)  # (x0,y0), (x1,y1)
    # cv2.rectangle(mask, (0, 0), (100, 35), 225, -1)
    cv2.rectangle(mask, (0, 88), (65, 95), 0, -1)
    cv2.rectangle(mask, (8, 103), (150, 135), 0, -1)  # hides the bar

    # cv2.rectangle(mask, (0, 95), (40, 144), 255, -1)

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\init\\pass_mask.png', mask)


def move_selector():
    img = cv2.imread('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\move\\3\\3.png')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = np.zeros(img.shape[:2], dtype="uint8")
    cv2.rectangle(mask, (40, 100), (46, 137), 254, -1)

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\move\\3\\3_mask.png', mask)



def pokedex_that_pops_up_after_caught_new_pk():
    img = cv2.imread('/fight/templates/states/pokedex/pokedex.tmp')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = np.zeros(img.shape[:2], dtype="uint8")
    cv2.rectangle(mask, (0, 72), (160, 79), 254, -1)

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite('/fight/templates/states/pokedex/pokedex_mask.msk', mask)

def game_menu():

    img = cv2.imread('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\game_menu\\item\\item.png')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = np.zeros(img.shape[:2], dtype="uint8")
    cv2.rectangle(mask, (80, 0), (160, 127), 254, -1)

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\game_menu\\item\\item_mask.png', mask)



def page_move():
    img = cv2.imread('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\pokemon_stats\\page_moves\\page_moves.tmp')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = 254*np.ones(img.shape[:2], dtype="uint8")    # choose a white (254* ones) or black (zeros) mask to start with

    cv2.rectangle(mask, (0, 0), (150, 55), 0, -1)
    cv2.rectangle(mask, (0, 55), (60, 63), 0, -1)
    cv2.rectangle(mask, (10, 72), (150, 135), 0, -1)

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\pokemon_stats\\page_moves\\page_moves_mask.png', mask)

def stats_page_stats():
    img = cv2.imread(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\pokemon_stats\\page_stats\\page_stats.tmp')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = 254 * np.ones(img.shape[:2], dtype="uint8")  # choose a white (254* ones) or black (zeros) mask to start with

    cv2.rectangle(mask, (0, 0), (152, 55), 0, -1)
    cv2.rectangle(mask, (0, 55), (60, 63), 0, -1)
    cv2.rectangle(mask, (7, 72), (70, 135), 0, -1)
    cv2.rectangle(mask, (80, 72), (150, 135), 0, -1)

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\pokemon_stats\\page_stats\\page_stats_mask.png',
        mask)

def pkmn_menu():
    img = cv2.imread(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\pkmn\\pkmn.png')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = 254 * np.ones(img.shape[:2], dtype="uint8")  # choose a white (254* ones) or black (zeros) mask to start with

    cv2.rectangle(mask, (0, 0), (160, 95), 0, -1)
    # cv2.rectangle(mask, (0, 55), (60, 63), 0, -1)
    # cv2.rectangle(mask, (7, 72), (150, 135), 0, -1)
    # cv2.rectangle(mask, (80, 72), (150, 135), 0, -1)

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\pkmn\\pkmn_mask.png',
        mask)

def game_menu_state():
    img = cv2.imread(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\game_menu\\game_menu.tmp')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = 254 * np.ones(img.shape[:2], dtype="uint8")  # choose a white (254* ones) or black (zeros) mask to start with

    cv2.rectangle(mask, (0, 0), (80, 144), 0, -1)
    cv2.rectangle(mask, (87, 60), (150, 74), 0, -1)
    cv2.rectangle(mask, (87, 10), (93, 120), 0, -1)
    cv2.rectangle(mask, (0, 127), (160, 144), 0, -1)
    # cv2.rectangle(mask, (0, 55), (60, 63), 0, -1)
    # cv2.rectangle(mask, (7, 72), (150, 135), 0, -1)
    # cv2.rectangle(mask, (80, 72), (150, 135), 0, -1)

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\game_menu\\game_menu_mask.png',
        mask)

def stats_or_switch_state():
    img = cv2.imread(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\stats_or_switch\\stats_or_switch.tmp')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = 254 * np.ones(img.shape[:2], dtype="uint8")  # choose a white (254* ones) or black (zeros) mask to start with

    cv2.rectangle(mask, (0, 0), (160, 87), 0, -1)
    cv2.rectangle(mask, (0, 87), (85, 95), 0, -1)
    cv2.rectangle(mask, (95, 95), (101, 136), 0, -1)
    # cv2.rectangle(mask, (87, 60), (150, 74), 0, -1)
    # cv2.rectangle(mask, (87, 10), (93, 120), 0, -1)
    # cv2.rectangle(mask, (0, 127), (160, 144), 0, -1)
    # cv2.rectangle(mask, (0, 55), (60, 63), 0, -1)
    # cv2.rectangle(mask, (7, 72), (150, 135), 0, -1)
    # cv2.rectangle(mask, (80, 72), (150, 135), 0, -1)

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\stats_or_switch\\stats_or_switch_mask.png',
        mask)


def switch_or_stats_choose():
    img = cv2.imread(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\party_menu\\stats\\stats.png')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = 254 * np.zeros(img.shape[:2],
                          dtype="uint8")  # choose a white (254* ones) or black (zeros) mask to start with

    # cv2.rectangle(mask, (0, 0), (160, 87), 0, -1)
    # cv2.rectangle(mask, (0, 87), (85, 95), 0, -1)

    cv2.rectangle(mask, (95, 95), (102, 136), 254, -1)
    # cv2.rectangle(mask, (87, 60), (150, 74), 0, -1)
    # cv2.rectangle(mask, (87, 10), (93, 120), 0, -1)
    # cv2.rectangle(mask, (0, 127), (160, 144), 0, -1)
    # cv2.rectangle(mask, (0, 55), (60, 63), 0, -1)
    # cv2.rectangle(mask, (7, 72), (150, 135), 0, -1)
    # cv2.rectangle(mask, (80, 72), (150, 135), 0, -1)

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\party_menu\\stats\\switch_or_stats_mask.png',
        mask)

def praty_menu_cursor():
    img = cv2.imread(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\party_menu\\0\\party_menu_0.png')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = 254 * np.ones(img.shape[:2], dtype="uint8")  # choose a white (254* ones) or black (zeros) mask to start with

    #cv2.rectangle(mask, (8, 0), (160, 95), 0, -1)
    cv2.rectangle(mask, (8, 0), (160, 95), 0, -1)
    # cv2.rectangle(mask, (87, 60), (150, 74), 0, -1)
    # cv2.rectangle(mask, (87, 10), (93, 120), 0, -1)
    # cv2.rectangle(mask, (0, 127), (160, 144), 0, -1)
    #cv2.rectangle(mask, (0, 55), (60, 63), 0, -1)
    #cv2.rectangle(mask, (7, 72), (150, 135), 0, -1)
    #cv2.rectangle(mask, (80, 72), (150, 135), 0, -1)

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\party_menu\\1\\party_menu_idx.png',
        mask)

def fight_init_trainer():
    img = cv2.imread('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\init_trainer\\fight_init_trainer.png')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = np.ones(img.shape[:2], dtype="uint8")
    cv2.rectangle(mask, (15, 23), (89, 10), 0, -1)
    cv2.rectangle(mask, (89, 0), (145, 87), 0, -1)  # (x0,y0), (x1,y1)
    #cv2.rectangle(mask, (0, 0), (80, 100), 225, -1)
    cv2.rectangle(mask, (8, 103), (150, 135), 0, -1)  # hides the bar

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite('C:\\Users\\oscar\\PcharmProjects\\Pokemon\\fight\\templates\\states\\init_trainer\\init_trainer_mask.png', mask)


def change_pokemon_after_fight():
    img = cv2.imread('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\change_pokemon\\fight_change_pokemon.tmp')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = np.ones(img.shape[:2], dtype="uint8")
    cv2.rectangle(mask, (15, 23), (89, 10), 0, -1)
    cv2.rectangle(mask, (80, 50), (145, 87), 0, -1)  # (x0,y0), (x1,y1)
    cv2.rectangle(mask, (80, 50), (160, 70), 0, -1)  # (x0,y0), (x1,y1)
    cv2.rectangle(mask, (48, 57), (60, 95), 0, -1)  #
    #cv2.rectangle(mask, (0, 0), (80, 100), 225, -1)
    cv2.rectangle(mask, (40, 103), (150, 120), 0, -1)

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\change_pokemon\\fight_change_pokemon_mask.png', mask)

def level_up():
    img = cv2.imread('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\level_up\\level_up.tmp')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = np.ones(img.shape[:2], dtype="uint8")
    cv2.rectangle(mask, (0, 0), (70, 95), 0, -1)

    cv2.rectangle(mask, (110, 32), (150, 38), 0, -1)  # (x0,y0), (x1,y1)
    cv2.rectangle(mask, (110, 48), (150, 54), 0, -1)  # (x0,y0), (x1,y1)
    cv2.rectangle(mask, (110, 64), (150, 70), 0, -1)  # (x0,y0), (x1,y1)
    cv2.rectangle(mask, (110, 80), (150, 87), 0, -1)  # (x0,y0), (x1,y1)

    cv2.rectangle(mask, (8, 103), (150, 135), 0, -1)  # hides the bar

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\level_up\\level_up.png', mask)


def yn_talk():
    img = cv2.imread('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\walk\\templates\\walk_states\\yn_talk\\yn_talk.tmp')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = np.ones(img.shape[:2], dtype="uint8")
    cv2.rectangle(mask, (0, 0), (70, 95), 0, -1)

    cv2.rectangle(mask, (0, 0), (111, 95), 0, -1)  # hides screen
    cv2.rectangle(mask, (0, 0), (160, 55), 0, -1)  # hides screen

    cv2.rectangle(mask, (8, 103), (150, 135), 0, -1)  # hides the bar

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()
    cv2.imwrite('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\walk\\templates\\walk_states\\yn_talk\\yn_talk_preview.png', masked)

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\walk\\templates\\walk_states\\yn_talk\\yn_talk_m.png', mask)


def start_menu():
    img = cv2.imread('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\gameplay\\templates\\states\\start_menu\\start_menu.tmp')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = np.ones(img.shape[:2], dtype="uint8")
    cv2.rectangle(mask, (8, 8), (14, 55), 0, -1)

    # cv2.rectangle(mask, (0, 0), (111, 95), 0, -1)  # hides screen
    # cv2.rectangle(mask, (0, 0), (160, 55), 0, -1)  # hides screen

    cv2.rectangle(mask, (0, 56), (160, 144), 0, -1)


    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()
    cv2.imwrite('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\gameplay\\templates\\states\\start_menu\\start_menu_preview.png', masked)

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\gameplay\\templates\\states\\start_menu\\start_menu_m.png', mask)

def start_menu_continue():
    img = cv2.imread(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\gameplay\\templates\\start_menu\\continue\\continue.tmp')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = np.ones(img.shape[:2], dtype="uint8")
    # cv2.rectangle(mask, (8, 8), (14, 55), 0, -1)

    # cv2.rectangle(mask, (0, 0), (111, 95), 0, -1)  # hides screen
    # cv2.rectangle(mask, (0, 0), (160, 55), 0, -1)  # hides screen

    cv2.rectangle(mask, (80, 65), (160, 144), 0, -1)

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\gameplay\\templates\\start_menu\\continue\\continue_preview.png',
        masked)

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\gameplay\\templates\\start_menu\\continue\\continue_m.png',
                mask)

def splash_screen():
    img = cv2.imread(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\gameplay\\templates\\states\\splash_screen\\splash_screen.tmp')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = np.ones(img.shape[:2], dtype="uint8")
    # cv2.rectangle(mask, (8, 8), (14, 55), 0, -1)

    # cv2.rectangle(mask, (0, 0), (111, 95), 0, -1)  # hides screen
    # cv2.rectangle(mask, (0, 0), (160, 55), 0, -1)  # hides screen

    cv2.rectangle(mask, (0, 65), (100, 144), 0, -1)

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\gameplay\\templates\\states\\splash_screen\\splash_screen_preview.png',
        masked)

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\gameplay\\templates\\states\\splash_screen\\splash_screen_m.png',
        mask)

def choose_name_menu():
    img = cv2.imread(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\gameplay\\templates\\states\\choose_player_name_menu\\choose_player_name_menu.tmp')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = np.ones(img.shape[:2], dtype="uint8")
    # cv2.rectangle(mask, (8, 8), (14, 55), 0, -1)

    # cv2.rectangle(mask, (0, 0), (111, 95), 0, -1)  # hides screen
    # cv2.rectangle(mask, (0, 0), (160, 55), 0, -1)  # hides screen

    cv2.rectangle(mask, (8, 10), (13, 80), 0, -1)

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\gameplay\\templates\\states\\choose_player_name_menu\\choose_player_name_menu_preview.png',
        masked)

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\gameplay\\templates\\states\\choose_player_name_menu\\choose_player_name_menu_m.png',
        mask)

def intro_story():
    img = cv2.imread(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\gameplay\\templates\\states\\start_story1\\start_story1.tmp')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = np.ones(img.shape[:2], dtype="uint8")
    # cv2.rectangle(mask, (8, 8), (14, 55), 0, -1)

    cv2.rectangle(mask, (8, 103), (150, 135), 0, -1)

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\gameplay\\templates\\states\\start_story1\\start_story1_preview.png',
        masked)

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\gameplay\\templates\\states\\start_story1\\start_story1_m.png',
        mask)

def market_menu():
    img = cv2.imread(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\walk\\templates\\market\\buy\\buy.tmp')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = np.ones(img.shape[:2], dtype="uint8")

    cv2.rectangle(mask, (8, 8), (13, 47), 225, -1)
    cv2.rectangle(mask, (95, 8), (150, 15), 0, -1)
    cv2.rectangle(mask, (110, 60), (126, 95), 0, -1)

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\walk\\templates\\market\\buy\\buy_preview.png',
        masked)

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\walk\\templates\\market\\buy\\buy_m.png',
                mask)

def amount_in_market():
    img = cv2.imread(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\gameplay\\templates\\market\\amount1\\amount1.tmp')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = 0 * np.ones(img.shape[:2], dtype="uint8")

    cv2.rectangle(mask, (56, 72), (95, 95), 255, -1)

    # cv2.rectangle(mask, (95, 8), (150, 15), 0, -1)
    # cv2.rectangle(mask, (110, 60), (126, 95), 0, -1)

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\gameplay\\templates\\market\\amount1\\amount1_preview.png',
        masked)

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\gameplay\\templates\\market\\amount1\\amount1_m.png',
                mask)


def buy_menu_state():
    img = cv2.imread(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\gameplay\\templates\\states\\buy_menu\\buy_menu.tmp')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = np.ones(img.shape[:2], dtype="uint8")

    # cv2.rectangle(mask, (8, 8), (13, 47), 0, -1)
    cv2.rectangle(mask, (95, 8), (150, 15), 0, -1)
    cv2.rectangle(mask, (40, 25), (150, 95), 0, -1)

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\gameplay\\templates\\states\\buy_menu\\buy_menu_preview.png',
        masked)

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\gameplay\\templates\\states\\buy_menu\\buy_menu_m.png',
                mask)


def buy_confirm():
    img = cv2.imread(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\gameplay\\templates\\states\\buy_confirm\\buy_confirm.tmp')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = np.ones(img.shape[:2], dtype="uint8")

    # cv2.rectangle(mask, (8, 8), (13, 47), 0, -1)
    cv2.rectangle(mask, (95, 8), (150, 15), 0, -1)
    cv2.rectangle(mask, (40, 25), (150, 55), 0, -1)
    cv2.rectangle(mask, (40, 25), (110, 70), 0, -1)
    cv2.rectangle(mask, (40, 25), (55, 95), 0, -1)

    cv2.rectangle(mask, (63, 80), (110, 88), 0, -1)  # price

    cv2.rectangle(mask, (8, 125), (150, 135), 0, -1)  # lower line in bar

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\gameplay\\templates\\states\\buy_confirm\\buy_confirm_preview.png',
        masked)

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\gameplay\\templates\\states\\buy_confirm\\buy_confirm_m.png',
        mask)

def buy_amount():
    img = cv2.imread(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\gameplay\\templates\\states\\buy_amount\\buy_amount.tmp')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = np.ones(img.shape[:2], dtype="uint8")

    # cv2.rectangle(mask, (8, 8), (13, 47), 0, -1)
    cv2.rectangle(mask, (95, 8), (150, 15), 0, -1)
    cv2.rectangle(mask, (40, 25), (150, 70), 0, -1)
    # cv2.rectangle(mask, (40, 25), (150, 70), 0, -1)
    cv2.rectangle(mask, (40, 25), (55, 95), 0, -1)

    cv2.rectangle(mask, (63, 80), (150, 88), 0, -1)  # price

    # cv2.rectangle(mask, (8, 125), (150, 135), 0, -1) # lower line in bar

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\gameplay\\templates\\states\\buy_amount\\buy_amount_preview.png',
        masked)

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\gameplay\\templates\\states\\buy_amount\\buy_amount_m.png',
                mask)

def walk_player():
    img = cv2.imread(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\walk\\templates\\map\\mask_create.png')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = np.ones(img.shape[:2], dtype="uint8")

    # cv2.rectangle(mask, (40, 25), (150, 70), 0, -1)
    cv2.rectangle(mask, (64, 56), (81, 75), 0, -1)

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\walk\\templates\\map\\mask_create_preview.png',
        masked)

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\walk\\templates\\map\\mask_create_m.png',
                mask)

def move_pokemon_where_cursor():
    img = cv2.imread(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\move_pokemon_where\\0\\move_pokemon_where0.png')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = 254 * np.ones(img.shape[:2], dtype="uint8")  # choose a white (254* ones) or black (zeros) mask to start with

    # cv2.rectangle(mask, (8, 0), (160, 95), 0, -1)
    cv2.rectangle(mask, (8, 0), (160, 95), 0, -1)
    # cv2.rectangle(mask, (87, 60), (150, 74), 0, -1)
    # cv2.rectangle(mask, (87, 10), (93, 120), 0, -1)
    # cv2.rectangle(mask, (0, 127), (160, 144), 0, -1)
    # cv2.rectangle(mask, (0, 55), (60, 63), 0, -1)
    # cv2.rectangle(mask, (7, 72), (150, 135), 0, -1)
    # cv2.rectangle(mask, (80, 72), (150, 135), 0, -1)

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\move_pokemon_where\\move_pokemon_where_preview.png',
        masked)

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\move_pokemon_where\\move_pokemon_where_m.png',
        mask)


def party_menu_without_bar():
    img = cv2.imread(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\party_menu\\0\\party_menu_0.png')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = 254 * np.ones(img.shape[:2], dtype="uint8")  # choose a white (254* ones) or black (zeros) mask to start with

    # cv2.rectangle(mask, (8, 0), (160, 95), 0, -1)
    cv2.rectangle(mask, (8, 0), (160, 95), 0, -1)
    cv2.rectangle(mask, (8, 103), (150, 135), 0, -1)  # hides the bar

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\party_menu\\0\\party_menu_0_preview.png',
        masked)

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\party_menu\\0\\party_menu_0_m.png',
        mask)

def use_next_pokemon():
    img = cv2.imread(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\use_next_pokemon\\use_next_pokemon.tmp')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = 254 * np.ones(img.shape[:2], dtype="uint8")  # choose a white (254* ones) or black (zeros) mask to start with

    # cv2.rectangle(mask, (8, 0), (160, 95), 0, -1)
    cv2.rectangle(mask, (0, 0), (160, 70), 0, -1)
    # cv2.rectangle(mask, (8, 103), (150, 135), 0, -1)  # hides the bar

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\use_next_pokemon\\use_next_pokemon_preview.png',
        masked)

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\use_next_pokemon\\use_next_pokemon_m.png',
        mask)

def bring_out_which_pokemon():
    img = cv2.imread(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\bring_out_which_pokemon\\bring_out.png')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = 254 * np.ones(img.shape[:2], dtype="uint8")  # choose a white (254* ones) or black (zeros) mask to start with

    # cv2.rectangle(mask, (8, 0), (160, 95), 0, -1)
    cv2.rectangle(mask, (0, 0), (160, 95), 0, -1)
    # cv2.rectangle(mask, (8, 103), (150, 135), 0, -1)  # hides the bar

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\bring_out_which_pokemon\\bring_out_preview.png',
        masked)

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\bring_out_which_pokemon\\bring_out_m.png',
        mask)

def no_will_to_fight():
    img = cv2.imread(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\no_will_to_fight\\no_will_to_fight.png')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = 254 * np.ones(img.shape[:2], dtype="uint8")  # choose a white (254* ones) or black (zeros) mask to start with

    # cv2.rectangle(mask, (8, 0), (160, 95), 0, -1)
    cv2.rectangle(mask, (0, 0), (160, 95), 0, -1)
    # cv2.rectangle(mask, (8, 103), (150, 135), 0, -1)  # hides the bar

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\no_will_to_fight\\no_will_to_fight_preview.png',
        masked)

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\no_will_to_fight\\no_will_to_fight_m.png',
        mask)


def stats_or_switch():
    img = cv2.imread(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\stats_or_switch\\stats_or_switch.tmp')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = 254 * np.ones(img.shape[:2], dtype="uint8")  # choose a white (254* ones) or black (zeros) mask to start with

    cv2.rectangle(mask, (0, 0), (160, 87), 0, -1)
    cv2.rectangle(mask, (0, 87), (85, 95), 0, -1)
    cv2.rectangle(mask, (95, 95), (101, 136), 0, -1)

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\stats_or_switch\\stats_or_switch_preview.png',
        masked)

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\states\\stats_or_switch\\stats_or_switch_m.png',
        mask)





def talk():
    img = cv2.imread('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\walk\\templates\\walk_states\\yn_talk\\yn_talk.tmp')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = np.ones(img.shape[:2], dtype="uint8")
    cv2.rectangle(mask, (0, 0), (70, 95), 0, -1)

    cv2.rectangle(mask, (0, 0), (111, 95), 0, -1)  # hides screen
    cv2.rectangle(mask, (0, 0), (160, 55), 0, -1)  # hides screen

    cv2.rectangle(mask, (8, 103), (150, 135), 0, -1)  # hides the bar

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()
    cv2.imwrite('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\walk\\templates\\walk_states\\yn_talk\\yn_talk_preview.png', masked)

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\walk\\templates\\walk_states\\yn_talk\\yn_talk_m.png', mask)


def buy_no_money():
    img = cv2.imread(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\gameplay\\templates\\states\\buy_no_money\\buy_no_money.tmp')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = np.ones(img.shape[:2], dtype="uint8")

    # cv2.rectangle(mask, (8, 8), (13, 47), 0, -1)
    cv2.rectangle(mask, (95, 8), (150, 15), 0, -1)
    cv2.rectangle(mask, (40, 25), (150, 70), 0, -1)
    # cv2.rectangle(mask, (40, 25), (150, 70), 0, -1)
    cv2.rectangle(mask, (40, 25), (55, 95), 0, -1)

    cv2.rectangle(mask, (63, 80), (150, 88), 0, -1)  # price

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\gameplay\\templates\\states\\buy_no_money\\buy_no_money_preview.png',
        masked)

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\gameplay\\templates\\states\\buy_no_money\\buy_no_money_m.png',
        mask)


def evolve():
    img = cv2.imread(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\pokebot\\fight\\templates\\states\\evolve\\evolve.png')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    mask = np.ones(img.shape[:2], dtype="uint8")

    # cv2.rectangle(mask, (8, 8), (13, 47), 0, -1)
    cv2.rectangle(mask, (0, 0), (160, 95), 0, -1)
    cv2.rectangle(mask, (50, 110), (150, 120), 0, -1)
    # cv2.rectangle(mask, (40, 25), (150, 70), 0, -1)
    # cv2.rectangle(mask, (40, 25), (55, 95), 0, -1)

    # cv2.rectangle(mask, (63, 80), (150, 88), 0, -1)  # price

    mask_view = cv2.resize(mask, (500, 500), interpolation=cv2.INTER_AREA)

    masked = cv2.bitwise_and(img, img, mask=mask)
    masked = cv2.resize(masked, (500, 500), interpolation=cv2.INTER_AREA)

    cv2.imshow('mask', masked)
    cv2.waitKey()
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\pokebot\\fight\\templates\\states\\evolve\\evolve_preview.png',
        masked)

    ''' afterwards change the name and extension to fight_menu.msk'''
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\pokebot\\fight\\templates\\states\\evolve\\evolve_m.png',
        mask)

def cursor():
    img = cv2.imread(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\cursor.png')

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('img', cv2.resize(img[40:49, 8:15], (500, 500), interpolation=cv2.INTER_AREA))
    cv2.waitKey()

    cv2.imshow('mask', img)
    cv2.waitKey()
    cv2.imwrite(
        'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\cursor_preview.png',
        img[40:49, 8:15])

