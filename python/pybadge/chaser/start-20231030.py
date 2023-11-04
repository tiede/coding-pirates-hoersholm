import board
import displayio
import terminalio
import time
import adafruit_imageload
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_pybadger import pybadger
import random

SCREEN_WIDTH = 160 
SCREEN_HEIGHT = 128

def intersect():
    circle_x1 = circle.x
    circle_x2 = circle.x + diameter
    circle_y1 = circle.y
    circle_y2 = circle.y + diameter

    rectangle_x1 = treat_sprite.x
    rectangle_x2 = treat_sprite.x + width
    rectangle_y1 = treat_sprite.y
    rectangle_y2 = treat_sprite.y + height

    intersect_left = rectangle_x1 < circle_x2
    intersect_right = rectangle_x2 > circle_x1
    intersect_top = rectangle_y1 < circle_y2
    intersect_bottom = rectangle_y2 > circle_y1

    if intersect_left and intersect_right and intersect_top and intersect_bottom:
        return True
    
    return False

def play_game_over_sound():
    A = 440
    G = 392
    C = 261
    E = 329

    pybadger.play_tone(C, duration=0.3)
    pybadger.play_tone(G, duration=0.1)
    pybadger.play_tone(A, duration=0.1)
    pybadger.play_tone(G, duration=0.1)
    pybadger.play_tone(E, duration=0.3)
    pybadger.play_tone(C, duration=0.4)

def play_sound():
    A = 440
    pybadger.play_tone(A, duration=0.1)

splash = displayio.Group()
board.DISPLAY.show(splash)

sprite_sheet, palette = adafruit_imageload.load("/two_sprites_halloween.bmp", 
                                                bitmap=displayio.Bitmap, 
                                                palette=displayio.Palette)

# treat sprite
treat_sprite = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                                  width=1,
                                  height=1,
                                  tile_width=20,
                                  tile_height=20,
                                  default_tile=1)

height = 20
width = 20
#rectangle = Rect(0, 0, width, height)
#rectangle.fill = 0x0000FF
#splash.append(rectangle)
splash.append(treat_sprite)

radius = 5
diameter = radius * 2
circle = Circle(80, 64, radius)
circle.fill = 0xFFFF00
splash.append(circle)

score = 0
text_score = label.Label(terminalio.FONT, text=str(score), color=0xFFFFFF, x=0, y=5)
splash.append(text_score)

level = 1
level_score = 0
text_level = label.Label(terminalio.FONT, text = "Level " + str(level), color=0xFFFFFF, x=0, y= 120)
splash.append(text_level)

text_game_over = label.Label(terminalio.FONT, text = "GAME OVER!!!", color=0xFF0000, x=20, y=int(SCREEN_HEIGHT/2), scale=2)

reset_game = False
game_over = False
game_stopped = False
speed = 500
rounds = 1
rounds_per_level = 5
ticks = 0
while True:

    if reset_game:
        score = 0
        level = 1
        rounds = 1
        ticks = 0
        speed = 500
        game_over = False
        game_stopped = False
        reset_game = False
        text_level.text = "Level " + str(level)
        if text_game_over in splash:
            splash.remove(text_game_over)

    if pybadger.button.start:
        reset_game = True

    if game_over:
        if not game_stopped:
            play_game_over_sound()
            splash.append(text_game_over)
            pybadger.pixels[0] = 0xFF0000
            game_stopped = True
            while not pybadger.button.start:
                time.sleep(0.1)
                text_game_over.color = 0x000000
                pybadger.pixels[0] = 0x000000
                time.sleep(0.1)
                text_game_over.color = 0xFF0000
                pybadger.pixels[0] = 0xFF0000
            reset_game = True
    else:
        if ticks == speed:
            while True:
                treat_sprite.x = random.randint(0, SCREEN_WIDTH - width)
                treat_sprite.y = random.randint(0, SCREEN_HEIGHT - height)
                if not intersect():
                    ticks = 0
                    rounds = rounds + 1
                    break

        if rounds == rounds_per_level:
            if level_score > 0:
                speed = int(speed - speed * 0.1)
                if speed < 100:
                    speed = 100
                rounds = 1
                level = level + 1
                level_score = 0
                text_level.text = "Level " + str(level)
                print (speed)
                print (ticks)
            else:
                game_over = True

        if pybadger.button.down:
            if circle.y < SCREEN_HEIGHT - diameter:
                circle.y = circle.y + 1
        if pybadger.button.up:
            if circle.y > 0: 
                circle.y = circle.y - 1
        if pybadger.button.left:
            if circle.x > 0:
                circle.x = circle.x - 1
        if pybadger.button.right:
            if circle.x < (SCREEN_WIDTH-diameter):
                circle.x = circle.x + 1

        if intersect():
            score = score + 1
            level_score = level_score + 1
            treat_sprite.x = -100
            treat_sprite.y = -100
            pybadger.pixels[0] = 0x0000FF
            pybadger.pixels[0] = 0x000000

        text_score.text = str(score)

        time.sleep(0.001)
        ticks = ticks + 1