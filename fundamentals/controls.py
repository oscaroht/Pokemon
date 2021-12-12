import time
from pynput.keyboard import Key, Controller

keyboard = Controller()

# control settings. Can be tuned using the function below
wait = 0.35
turnRatio = 0.03
goRatio = 0.068

def btnA(*argv):
    print("A")
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
    print("B")
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
    if len(args) == 0:
        n=1
    else:
        n = int(args[0])
    btnright(n, goRatio)

def goleft(*args):
    if len(args) == 0:
        n=1
    else:
        n = int(args[0])
    btnleft(n, goRatio)

def goup(*args):
    if len(args) == 0:
        n=1
    else:
        n = int(args[0])
    btnup(n, goRatio)

def godown(*args):
    if len(args) == 0:
        n=1
    else:
        n = int(args[0])
    btndown(n, goRatio)

def test1():
    '''' Meant to test the control settings. In order to do so find an area in the game where you can walk in a circle,
    run this function and visually assess Also check 'Options' -> 'Video' -> Vsync '''

    for i in range(8):
        turnright()
        goright()
        turndown()
        godown()
        turnleft()
        goleft()
        turnup()
        goup()

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

def test3():
    for i in range(4):
        turnright()
        turndown()
        turnleft()
        turnup()


if __name__ == '__main__':

    time.sleep(3)
    test1()
    test = 1