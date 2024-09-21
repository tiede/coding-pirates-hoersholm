import pygame
import random

SCREEN_X = 800
SCREEN_Y = 700
BANE_X = 300
BANE_Y = 600
BRIK = 30

# COLORS
WHITE = '#FFFFFF'
BLACK = '#000000'
RED = '#FF0000'
GREEN = '#00FF00'
BLUE = '#0000FF'
YELLOW = '#FFFF00'
ORANGE = '#FFA500'
MAGENTA = '#800000'
LIGHT_BLUE = '#00FFFF'

score = hiscore = 0

BRIK1 = [
    [
        '.....',
        '.XX..',
        '.XX..',
        '.....',
        '.....'
    ]
]

BRIK2 = [
    [
        '..X..',
        '..X..',
        '..X..',
        '..X..',
        '.....'
    ],
    [
        '.....',
        'XXXX.',
        '.....',
        '.....',
        '.....'
    ]
]

BRIK3 = [
    [
        '..X..',
        '..X..',
        '..XX.',
        '.....'
    ],
    [
        '.....',
        '.XXX.',
        '.X...',
        '.....'
    ],
    [
        '.....',
        '..XX.',
        '...X.',
        '...X.'
    ],
    [
        '.....',
        '...X.',
        '.XXX.',
        '.....'
    ]
]

BRIKLISTE = [BRIK1, BRIK2, BRIK3]
BRIKFARVER = [RED, GREEN, LIGHT_BLUE, YELLOW, ORANGE, BLUE, MAGENTA]

pygame.init()
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

clock = pygame.time.Clock()

class mitobjekt (object):
    def __init__(self, x, y, form):
        self.x = x
        self.y = y
        self.form = form
        self.farve = BRIKFARVER[BRIKLISTE.index(form)]
        self.rotation = 0

def lovlig_placering(brik, playing_field):
    accepteret_position = [[ (x,y) for x in range(10) if playing_field[y,x] == (0,0,0)] for y in range(20)]
    accepteret_position = [x for sub in accepteret_position for x in sub]

    return True

def get_center_x(rect):
    return SCREEN_X / 2 - rect.centerx

def show_start_screen():
    screen.fill(ORANGE)
    font = pygame.font.SysFont('Comic Sans', 80, bold=True)
    label = font.render('Tryk på en tast', 1, WHITE)
    screen.blit(label, (get_center_x(label.get_bounding_rect()),80))

    font = pygame.font.SysFont('Comic Sans', 60, bold=True)
    label = font.render('For at starte spillet', 1, WHITE)
    screen.blit(label, (get_center_x(label.get_bounding_rect()), 200))
    
    running = True
    returnValue = False
    while(running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                running = False
                returnValue = True
        clock.tick(60)
        pygame.display.update()

    # When we exit the user must have pressed a button
    return returnValue

def draw_grid(playing_field):
    pos_x = 50
    pos_y = 90
    for i in range(len(playing_field)):
        for j in range(len(playing_field[i])):
            color = playing_field[i][j]
            x1 = pos_x + j*BRIK
            y1 = pos_y + i*BRIK
            pygame.draw.rect(screen, color, pygame.Rect(x1, y1, BRIK, BRIK))
            pygame.draw.line(screen, GREEN, (pos_x + j*BRIK, pos_y), (pos_x + j*BRIK, pos_y + BANE_Y))
        pygame.draw.line(screen, GREEN, (pos_x, pos_y + i * BRIK), (pos_x+BANE_X, pos_y + i * BRIK))    
    
    # Draw a rect around the grid
    pygame.draw.rect(screen, RED, pygame.Rect(pos_x, pos_y, BANE_X, BANE_Y), width=2)

def update_playing_field(screen, playing_field):
    pos_x = 50
    pos_y = 90
    for i in range(len(playing_field)):
        for j in range(len(playing_field[i])):
            pygame.draw.rect(screen, playing_field[i][j], (pos_x + j * BRIK, pos_y + i*BRIK, BRIK, BRIK), 0)
    draw_grid(playing_field)

def start_game():
    screen.fill(BLACK)

    # Top
    font = pygame.font.SysFont('Comic Sans', 60, bold=True)
    label = font.render('Tetris', 1, WHITE)
    screen.blit(label, (30,10))
    font = pygame.font.SysFont('Comic Sans', 30, bold=True)
    label = font.render('By Coding Pirates Hørsholm', 1, WHITE)
    screen.blit(label, (230,42))

    # Score
    font = pygame.font.SysFont('Comic Sans', 40)
    label = font.render('Score ' + str(score), 1, YELLOW)
    screen.blit(label, (500, 110))

    # Næste brik
    font = pygame.font.SysFont('Comic Sans', 40)
    label = font.render('Næste brik ', 1, YELLOW)
    screen.blit(label, (500, 170))

    # Hiscore
    font = pygame.font.SysFont('Comic Sans', 40)
    label = font.render('Hi-score ' + str(hiscore), 1, ORANGE)
    screen.blit(label, (500, 600))

    playing_field = [[(BLACK) for _ in range(10)] for _ in range(20)]
    draw_grid(playing_field)

    next_tetromino = mitobjekt(1,0,random.choice(BRIKLISTE))
    format = next_tetromino.form[next_tetromino.rotation % len (next_tetromino.form)]
    pos_x = 500
    pos_y = 350
    for y, line in enumerate(format):
        row = list(line)
        for x, column in enumerate(row):
            if (column == 'X'):
                pygame.draw.rect(screen, next_tetromino.farve, (pos_x + x*BRIK, pos_y + y*BRIK, BRIK, BRIK), 0)

    ny_brik = mitobjekt(1,0, random.choice(BRIKLISTE))

    running = True
    while (running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    ny_brik.x -= 1
                elif event.key == pygame.K_RIGHT:
                    ny_brik.x += 1
                elif event.key == pygame.K_UP:
                    ny_brik.rotation += 1
                elif event.key == pygame.K_DOWN:
                    ny_brik.y += 1
        
        # Tegn ny brik på skærmen
        ny_brik_format = ny_brik.form[ny_brik.rotation % len(ny_brik.form)]
        placering = []

        for y, line in enumerate(ny_brik_format):
            row = list(line)
            for x, column in enumerate(row):
                if column == 'X':
                    placering.append((ny_brik.x + x, ny_brik.y + y))
                    #pygame.draw.rect(screen, ny_brik.farve, )

        for i, pos in enumerate(placering):
            placering[i] = (pos[0] - 1, pos[1] - 1)

        for i, pos in enumerate(placering):
            x, y = placering[i]
            if y > -1:
                playing_field[y][x] = ny_brik.farve
                
        update_playing_field(screen, playing_field)

        clock.tick(60)
        pygame.display.update()

if (show_start_screen()):
    start_game()

pygame.quit()
print ('Exited')