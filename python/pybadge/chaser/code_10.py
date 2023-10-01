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

    # https://silentmatt.com/rectangle-intersection/
    intersection_left = rectangle_x1 < circle_x2
    intersection_right = rectangle_x2 > circle_x1
    intersection_top = rectangle_y1 < circle_y2
    intersection_bottom = rectangle_y2 > circle_y1

    if intersection_left and intersection_right and intersection_top and intersection_bottom:
        return True
    
    return False

splash = displayio.Group()
board.DISPLAY.show(splash)

height = 20
width = 20
rectangle = Rect(80, 80, width, height)
rectangle.fill = 0x0000FF
splash.append(rectangle)

radius = 5
diameter = radius * 2
circle = Circle(80, 64, radius)
circle.fill = 0xFFFF00
splash.append(circle)

score = 0
font = terminalio.FONT
text = str(score)
color = 0xFFFFFF
text_score = label.Label(font, text=text, color=color, x=0, y=5)
splash.append(text_score)

ticks = 0
speed = 500
level_changes = 5000
level = 1
level_score = 0
game_over = False
game_stopped = False

text_level = label.Label(font, text="Level " + str(level), color=color, x=0, y=128-5)
splash.append(text_level)

while True:
    if game_over:
        if not game_stopped:
            text_area_game_over = label.Label(font, text="GAME OVER", color=0xFF0000, x=50, y=64)
            splash.append(text_area_game_over)
        game_stopped = True

    else:
        if ticks % speed == 0:
            while True:
                rectangle_x = random.randint(0, SCREEN_WIDTH - width)
                rectangle_y = random.randint(0, SCREEN_HEIGHT - height)
                rectangle.x = rectangle_x
                rectangle.y = rectangle_y
                if not intersect():
                    break

        if ticks > 0 and ticks % level_changes == 0:
            if level_score > 0:
                speed = int(speed - speed * 0.1)
                level = level + 1
                level_score = 0
                text_level.text = "Level " + str(level)
            else:
                game_over = True

        if pybadger.button.down:
            if circle.y < SCREEN_HEIGHT - 1 - diameter:
                circle.y = circle.y + 1
        if pybadger.button.up:
            if circle.y > 0:
                circle.y = circle.y - 1
        if pybadger.button.left:
            if circle.x > 0:
                circle.x = circle.x - 1
        if pybadger.button.right:
            if circle.x < SCREEN_WIDTH - 1 - diameter:
                circle.x = circle.x + 1

        time.sleep(0.001)
        ticks = ticks + 1

        if intersect():
            score = score + 1
            level_score = level_score + 1
            # Skjul rektangel
            rectangle.x = -100
            rectangle.y = -100

        text_score.text = str(score)