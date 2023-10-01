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

splash = displayio.Group()
board.DISPLAY.show(splash)

rectangle = Rect(0, 0, 20, 20)
rectangle.fill = 0x0000FF
splash.append(rectangle)

radius = 5
diameter = radius * 2
circle = Circle(80, 64, radius)
circle.fill = 0xFFFF00
splash.append(circle)

ticks = 0
while True:
    if ticks % 500 == 0:
        rectangle_x = random.randint(0, SCREEN_WIDTH)
        rectangle_y = random.randint(0, SCREEN_HEIGHT)

        rectangle.x = rectangle_x
        rectangle.y = rectangle_y

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