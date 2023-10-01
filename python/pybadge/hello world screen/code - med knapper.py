import board
import displayio
import terminalio
# Label til tekst
from adafruit_display_text import label
# Badger gør det nemt at bruge fx knapper
from adafruit_pybadger import pybadger


SCREEN_WIDTH = 160
SCREEN_HEIGHT = 128

splash = displayio.Group()
board.DISPLAY.show(splash)

text = "Tryk paa en knap..."
font = terminalio.FONT
color = 0x0000FF

# Skift farve
color = 0xFF0010

text_area = label.Label(font, text=text, color=color)

# Flyt position
text_area.x = 1
text_area.y = 10

splash.append(text_area)

while True:
    if pybadger.button.a:
        # Det virker ikke
        text = "1. Du har trykket paa a"
        # Det virker
        #text_area.text = "2. Du har trykket paa a"
    #pass