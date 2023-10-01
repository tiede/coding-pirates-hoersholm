import board
import displayio
import terminalio
import time
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle


SCREEN_WIDTH = 160
SCREEN_HEIGHT = 128

splash = displayio.Group()
board.DISPLAY.show(splash)

rect = Rect(0,0,20,20)
rect.fill = 0xFF0010

circle = Circle(80,64,10)
circle.fill = 0x00FF00

splash.append(rect)
splash.append(circle)

while True:
    pass
