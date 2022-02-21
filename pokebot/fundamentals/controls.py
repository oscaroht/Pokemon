import time
from pynput.keyboard import Controller

keyboard = Controller()

# control settings. Can be tuned using the function below
wait = 0.400
turnRatio = 0.0033 # 0.003500 # 0.028
goRatio = 0.036 # 0.03500  # 0.068

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
    if n<0:
        raise Exception(f"Negative number of steps as input arg. This is not possible")
    btnright(n, goRatio)

def goleft(*args):
    if len(args) == 0:
        n=1
    else:
        n = int(args[0])
    if n<0:
        raise Exception(f"Negative number of steps as input arg. This is not possible")
    btnleft(n, goRatio)

def goup(*args):
    if len(args) == 0:
        n=1
    else:
        n = int(args[0])
    if n<0:
        raise Exception(f"Negative number of steps as input arg. This is not possible")
    btnup(n, goRatio)

def godown(*args):
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
        print(time.time() - start)
        turndown()
        start = time.time()
        godown()
        print(time.time() - start)
        turnleft()
        start = time.time()
        goleft()
        print(time.time() - start)
        turnup()
        start = time.time()
        goup()
        print(time.time() - start)

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
        print(f"Turn right")
        turnright()
        print(f"Turn down")
        turndown()
        print(f"Turn left")
        turnleft()
        print(f"Turn up")
        turnup()


if __name__ == '__main__':
    print(f"Test starts in.. 3 sec")
    time.sleep(1)
    print(f"Test starts in.. 2 sec")
    time.sleep(1)
    print(f"Test starts in.. 1 sec")
    time.sleep(1)
    test_circle()