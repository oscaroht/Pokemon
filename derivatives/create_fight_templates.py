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
