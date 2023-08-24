import board
import displayio
import time
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_text.label import Label

from paddle import Paddle
from ball import Ball

# Passer til Pybadge skærmen
SCREEN_WIDTH = 160
SCREEN_HEIGHT = 128

score = 0

fps = 60

def game_over():
    global score, fps
    score = 0
    fps = 60

def faaet_point():
    global score
    score = score + 1

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

# Tegn paddle
bredde = 5
hoejde = 30

paddle_hoejre = Paddle(bredde, hoejde, SCREEN_WIDTH - bredde, SCREEN_HEIGHT - hoejde, SCREEN_HEIGHT)
splash.append(paddle_hoejre.rect)

# Tegn bold
bold = Ball(3, 20, int(SCREEN_HEIGHT/2), SCREEN_HEIGHT, SCREEN_WIDTH)
splash.append(bold.circle)

# Score
score_label = Label(terminalio.FONT, text="0", color=0xFBCEB1) # x=int(SCREEN_WIDTH/2) - 5, y=5)
score_label.anchored_position = (int(SCREEN_WIDTH / 2), 0)
score_label.anchor_point = (0.5, 0)
splash.append(score_label)

sidst_opdateret = 0
nu = 0

while True:
    nu = time.monotonic()
    if sidst_opdateret + (1 / fps) <= nu:
        paddle_hoejre.update()
        bold.update(paddle_hoejre, faaet_point, game_over)
        score_label.text = str(score)

        sidst_opdateret = nu

    if score % 10 == 0 and score > 0 and fps < 120:
        fps = fps + 30