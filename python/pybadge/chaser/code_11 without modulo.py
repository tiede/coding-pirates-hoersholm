'''
Speaker
'''

import board
import displayio
import terminalio
import time
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_pybadger import pybadger
import random

SCREEN_WIDTH = 160 
SCREEN_HEIGHT = 128

def intersect():
    circle_x1 = circle.x
    circle_x2 = circle.x + diameter
    circle_y1 = circle.y
    circle_y2 = circle.y + diameter

    rectangle_x1 = rectangle.x
    rectangle_x2 = rectangle.x + width
    rectangle_y1 = rectangle.y
    rectangle_y2 = rectangle.y + height

    intersect_left = rectangle_x1 < circle_x2
    intersect_right = rectangle_x2 > circle_x1
    intersect_top = rectangle_y1 < circle_y2
    intersect_bottom = rectangle_y2 > circle_y1

    if intersect_left and intersect_right and intersect_top and intersect_bottom:
        return True
    
    return False

def play_game_over_sound():
    C = 261
    G = 392
    A = 440
    E = 329

    pybadger.play_tone(C, duration=0.3)
    pybadger.play_tone(G, duration=0.1)
    pybadger.play_tone(A, duration=0.1)
    pybadger.play_tone(G, duration=0.1)
    pybadger.play_tone(E, duration=0.3)
    pybadger.play_tone(C, duration=0.4)

splash = displayio.Group()
board.DISPLAY.show(splash)

height = 20
width = 20
rectangle = Rect(0, 0, width, height)
rectangle.fill = 0x0000FF
splash.append(rectangle)

radius = 5
diameter = radius * 2
circle = Circle(80, 64, radius)
circle.fill = 0xFFFF00
splash.append(circle)

score = 0
text_score = label.Label(terminalio.FONT, text=str(score), color=0xFFFFFF, x=0, y=5)
splash.append(text_score)

level = 1
level_score = 0
text_level = label.Label(terminalio.FONT, text="Level " + str(level), color=0xFFFFFF, x=0, y=128-5)
splash.append(text_level)

rounds = 1
rounds_per_level = 10
speed = 500
ticks = 0
game_over = False
game_stopped = False

play_game_over_sound()

while True:
    if game_over:
        if not game_stopped:
            text_area_game_over = label.Label(terminalio.FONT, text="GAME OVER", color=0xFF0000, x=50, y=64)
            splash.append(text_area_game_over)
            play_game_over_sound()
        game_stopped = True
    else:
        if ticks == speed:
            while True:
                rectangle_x = random.randint(0, SCREEN_WIDTH - width)
                rectangle_y = random.randint(0, SCREEN_HEIGHT - height)
                rectangle.x = rectangle_x
                rectangle.y = rectangle_y
                if not intersect():
                    break
            ticks = 0
            rounds = rounds + 1

        if rounds == rounds_per_level:
            if level_score > 0:
                speed = int(speed - speed * 0.1)
                rounds = 1
                level = level + 1
                level_score = 0
                text_level.text = "Level " + str(level)
            else:
                game_over = True

        if pybadger.button.down:
            if circle.y < SCREEN_HEIGHT - diameter:
                circle.y = circle.y + 1
        if pybadger.button.up:
            if circle.y > 0:
                circle.y = circle.y - 1
        if pybadger.button.left:
            if circle.x > 0:
                circle.x = circle.x - 1
        if pybadger.button.right:
            if circle.x < (SCREEN_WIDTH-diameter):
                circle.x = circle.x + 1

        if intersect():
            score = score + 1
            level_score = level_score + 1
            rectangle.x = -100
            rectangle.y = -100
            ticks = 250

        text_score.text = str(score)

        time.sleep(0.001)
        ticks = ticks + 1