import board
import displayio
import time
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle

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
hoejde = 20
paddle_venstre = Rect(0, 0, bredde, hoejde, fill=0x0)
splash.append(paddle_venstre)

paddle_hoejre = Rect(SCREEN_WIDTH - bredde, 0, bredde, hoejde, fill=0x0)
splash.append(paddle_hoejre)

sidst_opdateret = 0
nu = 0
nedad = True

while True:
    nu = time.monotonic()
    if sidst_opdateret + FPS_FORSINKELSE <= nu:
        if (nedad):
            paddle_venstre.y = paddle_venstre.y + 1
            paddle_hoejre.y = paddle_hoejre.y + 1
        else:
            paddle_venstre.y = paddle_venstre.y - 1
            paddle_hoejre.y = paddle_hoejre.y - 1

        if paddle_venstre.y>= SCREEN_HEIGHT - hoejde:
            nedad = False

        if (paddle_venstre.y <= 0):
            nedad = True

        sidst_opdateret = nu