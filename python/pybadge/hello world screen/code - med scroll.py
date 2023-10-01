import board
import displayio
import terminalio
import time
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

# Til FPS opdatering
sidst_opdateret = 0
nu = 0

while True:
    nu = time.monotonic()
    if sidst_opdateret + (1 / FPS) <= nu:
        # Rul tekst
        text_area.x = text_area.x + 1

        sidst_opdateret = nu

    if text_area.x > SCREEN_WIDTH:
        text_area.x = -100

    #pass