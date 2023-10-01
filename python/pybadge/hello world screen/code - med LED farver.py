import board
import displayio
import terminalio
import time
# Label til tekst
from adafruit_display_text import label
# Badger gør det nemt at bruge fx knapper
from adafruit_pybadger import pybadger

def wheel(pos):
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

pybadger.pixels[0] = (255,0,0)
#pybadger.pixels.fill((255,255,0))

pixels = pybadger.pixels
# r = 0
# g = 0
# b = 0

RED = (255, 0, 0)
ORANGE = (255, 191, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
#CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
INDIGO = (75,0,130)
#PURPLE = (180, 0, 255)
VIOLET = (238, 130, 238)

while True:

    # pixels.fill(RED)
    # time.sleep(1)
    # pixels.fill(ORANGE)
    # time.sleep(1)
    # pixels.fill(GREEN)
    # time.sleep(1)
    # pixels.fill(BLUE)
    # time.sleep(1)
    # pixels.fill(INDIGO)
    # time.sleep(1)
    # pixels.fill(VIOLET)
    # time.sleep(1)
    
    for j in range(256):  # one cycle of all 256 colors in the wheel
        color = wheel(j)
        print (color)
        pixels.fill(color)
        time.sleep(0.1)
        # for i in range(pixels.count()):
            # tricky math! we use each pixel as a fraction of the full 96-color wheel
            # (thats the i / strip.numPixels() part)
            # Then add in j which makes the colors go around per pixel
            # the % 96 is to make the wheel cycle around
            # pixels.set_pixel(i, wheel(((i * 256 // pixels.count()) + j) % 256) )
            # pixels.show()
            # if wait > 0:
            #    time.sleep(wait)


    pass