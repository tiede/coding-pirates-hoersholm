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

# Tegn et kors
midt_x = int(SCREEN_WIDTH / 2)
midt_y = int(SCREEN_HEIGHT / 2)
for i in range(0, SCREEN_WIDTH):
    color_bitmap[i, midt_y - 1] = 1
    color_bitmap[i, midt_y] = 1
    color_bitmap[i, midt_y + 1] = 1

for i in range(0, SCREEN_HEIGHT):
    color_bitmap[midt_x - 1, i] = 1
    color_bitmap[midt_x, i] = 1
    color_bitmap[midt_x + 1, i] = 1

while True:
    pass