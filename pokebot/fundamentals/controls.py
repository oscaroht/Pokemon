import time
from pynput.keyboard import Controller, Key
import logging
logger = logging.getLogger(__name__)

keyboard = Controller()

# control settings. Can be tuned using the function below
wait = 0.400
turnRatio = 0.0035 # 0.003500 # 0.028
goRatio = 0.042 # 0.03500  # 0.068
# I want go to take 0.45 seconds

def adjust_go_ratio(measured_time, desired_time = 0.45, threshold=0.01):
    global goRatio
    increase = desired_time/measured_time
    if abs(increase-1) >= threshold:
        logger.debug(f"New button hold time {round(increase*100)} % of old hold time")
        goRatio *= increase

def btnF(number):
    f_map = {1:Key.f1,
           2:Key.f2,
           3:Key.f3,
           4:Key.f4,
           5:Key.f5,
           6:Key.f6,
           7:Key.f7,
           8:Key.f8,
           9:Key.f9,
           10:Key.f10,
           11:Key.f11,
           12:Key.f12}

    keyboard.press(f_map[number])
    time.sleep(1)
    keyboard.release(f_map[number])

def btn_save(number):
    f_map = {1:Key.f1,
           2:Key.f2,
           3:Key.f3,
           4:Key.f4,
           5:Key.f5,
           6:Key.f6,
           7:Key.f7,
           8:Key.f8,
           9:Key.f9,
           10:Key.f10
             }

    keyboard.press(Key.shift)
    keyboard.press(f_map[number])
    time.sleep(1)
    keyboard.release(f_map[number])
    keyboard.release(Key.shift)

def btnA(*argv):
    logger.debug("A")
    if len(argv) == 0:
        n=1
    else:
        n = int(argv[0])

    for i in range(n):
        keyboard.press('z')
        time.sleep(1)
        keyboard.release('z')
        time.sleep(1)

def btnB(*args):
    logger.debug("B")
    if len(args) == 0:
        n=1
    else:
        n = int(args[0])

    for i in range(n):
        keyboard.press('x')
        time.sleep(1)
        keyboard.release('x')
        time.sleep(1)

def btnup(n, m):
    for i in range(n):
        keyboard.press('w')
        time.sleep(m)
        keyboard.release('w')
        time.sleep(wait)

def btndown(n, m):
    for i in range(n):
        keyboard.press('s')
        time.sleep(m)
        keyboard.release('s')
        time.sleep(wait)

def btnright(n, m):
    for i in range(n):
        keyboard.press('d')
        time.sleep(m)
        keyboard.release('d')
        time.sleep(wait)

def btnleft(n, m):
    for i in range(n):
        keyboard.press('a')
        time.sleep(m)
        keyboard.release('a')
        time.sleep(wait)

def btnStart():
    keyboard.press('f')
    time.sleep(0.3)
    keyboard.release('f')
    time.sleep(0.3)

def turnright():
    btnright(1, turnRatio)

def turnleft():
    btnleft(1, turnRatio)

def turnup():
    btnup(1, turnRatio)

def turndown():
    btndown(1, turnRatio)


def goright(*args):
    logger.debug(f"Go ratio is now {goRatio}")
    if len(args) == 0:
        n=1
    else:
        n = int(args[0])
    if n<0:
        raise Exception(f"Negative number of steps as input arg. This is not possible")
    btnright(n, goRatio)

def goleft(*args):
    logger.debug(f"Go ratio is now {goRatio}")
    if len(args) == 0:
        n=1
    else:
        n = int(args[0])
    if n<0:
        raise Exception(f"Negative number of steps as input arg. This is not possible")
    btnleft(n, goRatio)

def goup(*args):
    logger.debug(f"Go ratio is now {goRatio}")
    if len(args) == 0:
        n=1
    else:
        n = int(args[0])
    if n<0:
        raise Exception(f"Negative number of steps as input arg. This is not possible")
    btnup(n, goRatio)

def godown(*args):
    logger.debug(f"Go ratio is now {goRatio}")
    if len(args) == 0:
        n=1
    else:
        n = int(args[0])
    if n<0:
        raise Exception(f"Negative number of steps as input arg. This is not possible")
    btndown(n, goRatio)

def test_circle():
    '''' Meant to test the control settings. In order to do so find an area in the game where you can walk in a circle,
    run this function and visually assess Also check 'Options' -> 'Video' -> Vsync '''

    for i in range(8):
        turnright()
        start = time.time()
        goright()
        logger.debug(time.time() - start)
        turndown()
        start = time.time()
        godown()
        logger.debug(time.time() - start)
        turnleft()
        start = time.time()
        goleft()
        logger.debug(time.time() - start)
        turnup()
        start = time.time()
        goup()
        logger.debug(time.time() - start)

def test2():

    for i in range(4):
        turnright()
        goright()
        turndown()
        godown()
        turnleft()
        goleft()
        turnup()
        goup()
        turnleft()
        goleft()
        turndown()
        godown()
        turnright()
        goright()
        turnup()
        goup()

def test_turn():
    for i in range(4):
        logger.debug(f"Turn right")
        turnright()
        logger.debug(f"Turn down")
        turndown()
        logger.debug(f"Turn left")
        turnleft()
        logger.debug(f"Turn up")
        turnup()


if __name__ == '__main__':
    logger.debug(f"Test starts in.. 3 sec")
    time.sleep(1)
    logger.debug(f"Test starts in.. 2 sec")
    time.sleep(1)
    logger.debug(f"Test starts in.. 1 sec")
    time.sleep(1)
    btnF(12)
