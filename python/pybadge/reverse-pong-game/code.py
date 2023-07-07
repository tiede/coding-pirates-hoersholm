import board
import displayio
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle

# Passer til Pybadge skærmen
SCREEN_WIDTH = 160
SCREEN_HEIGHT = 128

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

while True:
    pass