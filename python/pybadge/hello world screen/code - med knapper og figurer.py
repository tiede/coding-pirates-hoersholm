import board
import displayio
import terminalio
import time
# Badger gør det nemt at bruge fx knapper
from adafruit_display_shapes.circle import Circle
from adafruit_pybadger import pybadger

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 128

splash = displayio.Group()
board.DISPLAY.show(splash)

circle = Circle(5,5,5)
circle.fill = 0xFF00FF
splash.append(circle)


while True:
    if pybadger.button.up:
        circle.y = circle.y - 1
    elif pybadger.button.down:
        circle.y = circle.y + 1
    elif pybadger.button.left:
        circle.x = circle.x -1
    elif pybadger.button.right:
        circle.x = circle.x + 1
    time.sleep(0.02)
