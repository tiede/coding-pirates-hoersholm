import board
import displayio
import time
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle

from paddle import Paddle
from ball import Ball

# Passer til Pybadge skærmen
SCREEN_WIDTH = 160
SCREEN_HEIGHT = 128

FPS = 60
FPS_FORSINKELSE = 1 / FPS

# Lav display
splash = displayio.Group()
board.DISPLAY.show(splash)

# Lav baggrund med farven 0x1177bb
color_bitmap = displayio.Bitmap(SCREEN_WIDTH, SCREEN_HEIGHT, 2)
color_palette = displayio.Palette(2)
color_palette[0] = 0x1177bb
color_palette[1] = 0xFFFF00
bg_sprite = displayio.TileGrid(color_bitmap, x=0, y=0, pixel_shader=color_palette)
splash.append(bg_sprite)

# Tegn paddles
bredde = 5
hoejde = 30

paddle_venstre = Paddle(bredde, hoejde, 0, 0, SCREEN_HEIGHT)
splash.append(paddle_venstre.rect)

paddle_hoejre = Paddle(bredde, hoejde, SCREEN_WIDTH - bredde, SCREEN_HEIGHT - hoejde, SCREEN_HEIGHT)
splash.append(paddle_hoejre.rect)

# Tegn bold
bold = Ball(3, int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2), SCREEN_HEIGHT, SCREEN_WIDTH)
splash.append(bold.circle)

sidst_opdateret = 0
nu = 0

while True:
    nu = time.monotonic()
    if sidst_opdateret + FPS_FORSINKELSE <= nu:
        paddle_venstre.update()
        paddle_hoejre.update()
        bold.update(paddle_venstre, paddle_hoejre)

        sidst_opdateret = nu