import time
import random
import os
import sys
import termios
import tty
import select

WIDTH = 21
HEIGHT = 11

snake = [(11, 6)]
direction = "+x"

food = (13, 6)

def get_key():
    if select.select([sys.stdin], [], [], 0)[0]:
        key = sys.stdin.read(1)

        if key == "\x1b":
            key += sys.stdin.read(2)

            if key == "\x1b[A":
                return "UP"
            elif key == "\x1b[B":
                return "DOWN"
            elif key == "\x1b[C":
                return "RIGHT"
            elif key == "\x1b[D":
                return "LEFT"

    return None

old_settings = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin.fileno())

def move(unit, dx=0, dy=0):
    old_head = unit[0]

    x = old_head[0] + dx
    y = old_head[1] + dy

    if x >= WIDTH:
        x = 0
    elif x < 0:
        x = WIDTH - 1

    if y >= HEIGHT:
        y = 0
    elif y < 0:
        y = HEIGHT - 1

    for i in range(len(unit) - 1, 0, -1):
        unit[i] = unit[i - 1]

    unit[0] = (x, y)

def eat(unit):
    global food

    new_food = (
        random.randrange(WIDTH),
        random.randrange(HEIGHT)
    )

    if new_food in unit:
        return eat(unit)

    unit.append(unit[-1])
    food = new_food

try:
    while True:
        key = get_key()

        if key == "UP":
            direction = "-y"
        elif key == "DOWN":
            direction = "+y"
        elif key == "LEFT":
            direction = "-x"
        elif key == "RIGHT":
            direction = "+x"

        print("\033[H", end="")

        for y in range(HEIGHT):
            line = ""

            for x in range(WIDTH):
                if (x, y) == food and (x, y) != snake[0]:
                    line += "*"
                elif (x, y) == snake[0]:
                    line += "@"
                elif (x, y) in snake and (x, y) != snake[0]:
                    line += "O"
                else:
                    line += "."

            print(line)

        if direction == "+x":
            move(snake, 1, 0)

            if snake[0] == food:
                eat(snake)

        elif direction == "-x":
            move(snake, -1, 0)

            if snake[0] == food:
                eat(snake)

        elif direction == "+y":
            move(snake, 0, 1)

            if snake[0] == food:
                eat(snake)

        elif direction == "-y":
            move(snake, 0, -1)

            if snake[0] == food:
                eat(snake)

        time.sleep(0.4)

finally:
    termios.tcsetattr(
        sys.stdin,
        termios.TCSADRAIN,
        old_settings
    )
