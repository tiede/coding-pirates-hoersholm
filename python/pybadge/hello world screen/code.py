import board
import displayio
import terminalio
import time
import random
from adafruit_display_text import label


SCREEN_WIDTH = 160
SCREEN_HEIGHT = 128
FPS = 60

splash = displayio.Group()
board.DISPLAY.show(splash)

text = "Hej kodepirater"
font = terminalio.FONT
color = 0x0000FF

# Skift farve
color = 0xFF0010

text_area = label.Label(font, text=text, color=color)

# Flyt position
text_area.x = 10
text_area.y = 10

splash.append(text_area)

inc = 1

while True:
    text_area.x = text_area.x + inc

    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    if text_area.x > SCREEN_WIDTH - 88:
        inc = -1
        text_area.color = (r,g,b)

    elif text_area.x < 0:
        inc = 1
        text_area.color = (r,g,b)

    time.sleep(0.015)
