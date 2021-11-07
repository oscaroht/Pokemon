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
    cv2.rectangle(mask, (142, 127), (152, 136), 255, -1)

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


img = cv2.imread(
    'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\party_menu\\stats\\stats.png')

img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
cv2.imshow('img', cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA))
cv2.waitKey()

mask = 254 * np.zeros(img.shape[:2], dtype="uint8")  # choose a white (254* ones) or black (zeros) mask to start with

#cv2.rectangle(mask, (0, 0), (160, 87), 0, -1)
#cv2.rectangle(mask, (0, 87), (85, 95), 0, -1)

cv2.rectangle(mask, (95, 95), (102, 136), 254, -1)
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
    'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\fight\\templates\\party_menu\\stats\\switch_or_stats_mask.png',
    mask)
