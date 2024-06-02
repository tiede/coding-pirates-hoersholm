# importere de funktioner vi skal bruge

import pygame
import random

pygame.font.init()
#pygame.init()

# Standard vaerdier

SKAERM_X = 800
SKAERM_Y = 700
BANE_X = 300
BANE_Y = 600
BRIK = 30

# Mine standardfarver
WHITE = '#FFFFFF'
BLACK = '#000000'
#RED = (255,0,0)
#RED2 = 0xFF0000
RED = '#FF0000'
GREEN = '#00FF00'
BLUE = '#0000FF'
YELLOW = '#FFFF00'
ORANGE = '#FFA500'
MAGENTA = '#800000'
LIGHT_BLUE = '#00FFFF'

score = 0
highscore = 0

BRIK1 = [
    ['.....',
     '.XX..',
     '.XX..',
     '.....',
     '.....']
     ]

BRIK2 = [
    ['..X..',
     '..X..',
     '..X..',
     '..X..',
     '.....'],
    ['.....',
     'XXXX.',
     '.....',
     '.....',
     '.....']]

BRIK3 = [
    ['..X..',
     '..X..',
     '..XX.',
     '.....',
     ],
    ['.....',
     '.XXX.',
     '.X...',
     '.....',
     ],
    ['.....',
     '..XX.',
     '...X.',
     '...X.',
     ],
    ['.....',
     '...X.',
     '.XXX.',
     '.....',
     ]
]

BRIKLISTE = [BRIK1, BRIK2,BRIK3]
BRIKFARVER = [RED, GREEN, LIGHT_BLUE, YELLOW, ORANGE, BLUE, MAGENTA]

# startbillede
def startskaerm():
    # baggrundsfarven
    skaerm = pygame.display.set_mode((SKAERM_X,SKAERM_Y))
    skaerm.fill(ORANGE)
    
    # tekstlinje 1
    font = pygame.font.SysFont("comicsans",80 , bold=True)
    label = font.render("Tryk på en tast",1,WHITE)
    skaerm.blit(label,(80,200))

    # tekstlinje 2
    font = pygame.font.SysFont("comicsans",60 , bold=True)
    label = font.render('for at starte',1,WHITE)
    skaerm.blit(label,(200,300))

    # Vi skal lige opdatere skaermen
    pygame.display.update()

    vent = True
    while vent:
        for knap in pygame.event.get():
            if knap.type == pygame.quit:
                vent = False

            if knap.type == pygame.KEYDOWN:
                vent = False
                # saa skal vi lave selve spillet og starte det

def tegngitter(skaerm, bane):
    pos_x = 50
    pos_y = 90
    for i in range(len(bane)):
        pygame.draw.line(skaerm, GREEN, (pos_x, pos_y + i*BRIK), (pos_x+BANE_X, pos_y+ i*BRIK)) #VANDRETTE
        for j in range(len(bane[i])):
            pygame.draw.line(skaerm, GREEN, (pos_x + j*BRIK, pos_y),(pos_x + j*BRIK, pos_y + BANE_Y)) #LODRETTE

    #tegn ramme
    pygame.draw.rect(skaerm, RED, (pos_x, pos_y, BANE_X+2, BANE_Y+2), 5)

def opdater_bane(skaerm,bane):
    pos_x = 50
    pos_y = 90
    for i in range(len(bane)):
        for j in range(len(bane[i])):
            pygame.draw.rect(skaerm,bane[i][j],(pos_x + j*BRIK, pos_y + i*BRIK, BRIK, BRIK),0)        

    #tegn ramme
    pygame.draw.rect(skaerm, RED, (pos_x, pos_y, BANE_X+2, BANE_Y+2), 5)
    tegngitter(skaerm,bane)
    pygame.display.update()        

class mitobjekt(object):
    def __init__(self, x, y, form):
        self.x = x
        self.y = y
        self.form = form
        self.farve = BRIKFARVER[BRIKLISTE.index(form)]
        self.rotation = 0

def tegnbane(brugteplaceringer = {}):
    bane = [[(0,0,0) for _ in range(10)] for _ in range(20)]
    for y in range(len(bane)):
        for x in range(len(bane[y])):
            if (y,x) in brugteplaceringer:
                farve = brugteplaceringer[(y,x)]
                bane[y][x] = farve
    return bane

def lovlig_placering(brik, bane):
    accepteret_position = [[ (x,y) for x in range(10) if bane[y][x] == (0,0,0)] for y in range(20)]
    accepteret_position = [x for sub in accepteret_position for x in sub]

    return True

def fjern_raekke(bane, brugteplaceringer):
    taeller = 0
    for x in range(len(bane) - 1, -1, -1):
        raekke = bane[x]
        if (0,0,0) not in raekke:
            taeller += 1
            test = 1
            for y in range(len(raekke)):
                try:
                    del brugteplaceringer[(y,x)]
                except:
                    continue

    if taeller > 1:
        for key in sorted(list(brugteplaceringer), key = lambda x : x[1]) [::-1]:
            x, y = key
            if y < test:
                newkey = (x,y + taeller)
                brugteplaceringer[newkey] = brugteplaceringer.pop(key)
                return taeller

def spillet():
    # baggrundsfarven
    skaerm = pygame.display.set_mode((SKAERM_X,SKAERM_Y))
    skaerm.fill(BLACK)

    # tegn gitter
    bane = [[(BLACK) for _ in range(10)] for _ in range(20)]
    tegngitter(skaerm,bane)    

    # tegn overskrift
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris - Coding Pirates', 1, WHITE)
    skaerm.blit(label, (80, 10))
    
    # tegn score
    font = pygame.font.SysFont('comicsans', 40)
    label = font.render('Score: ' + str(score), 1, WHITE)
    skaerm.blit(label, (400, 200))

    # tegn hiscore
    font = pygame.font.SysFont('comicsans', 40)
    label = font.render('High Score: ' + str(highscore), 1, WHITE)
    skaerm.blit(label, (400, 600))

    # Naeste brik
    font = pygame.font.SysFont('comicsans', 40)
    label = font.render('Næste brik:', 1, WHITE)
    skaerm.blit(label, (400, 275))

    # Lad os tegne den naeste brik
    naestebrik = mitobjekt(1,0,random.choice(BRIKLISTE))
    format = naestebrik.form[naestebrik.rotation % len(naestebrik.form)]
    pos_x = 420
    pos_y = 350
    for y, line in enumerate(format):
        row = list(line)
        for x, column in enumerate(row):
            if column == 'X':
                pygame.draw.rect(skaerm,naestebrik.farve, (pos_x + x*BRIK, pos_y + y*BRIK, BRIK, BRIK), 0)

    # Så skal vi lige den aktuelle brik vi skal flytte rundt paa
    ny_brik = mitobjekt(1,0,random.choice(BRIKLISTE))

    # Vi skal lige opdatere skaermen
    pygame.display.update()

    brugteplaceringer = {}
    vent = True
    while vent:
        bane = tegnbane(brugteplaceringer)
        for knap in pygame.event.get():
            if knap.type == pygame.quit:
                vent = False
                pygame.display.quit()
            elif knap.type == pygame.KEYDOWN:
                if knap.key == pygame.K_LEFT:
                    print("Venstre")
                    ny_brik.x -= 1
                    if not(lovlig_placering(ny_brik, bane)):
                        ny_brik.x += 1
                elif knap.key == pygame.K_RIGHT:
                    print("Højre")
                    ny_brik.x += 1
                    if not(lovlig_placering(ny_brik, bane)):
                        ny_brik.x -= 1
                elif knap.key == pygame.K_UP:
                    print("Op")
                    ny_brik.rotation += 1 # Vi roterer mod hoere hvis minus roterer vi mod venstre
                    if not(lovlig_placering(ny_brik, bane)):
                        ny_brik.rotation -= 1
                elif knap.key == pygame.K_DOWN:
                    print("Ned")
                    ny_brik.y += 1
                    if not(lovlig_placering(ny_brik, bane)):
                        ny_brik.y -= 1
                elif knap.key == pygame.K_SPACE:
                    print("farvel")
                    pygame.display.quit()

        # så skal vi tegne ny_brik paa skaermen
        format = ny_brik.form[ny_brik.rotation % len(ny_brik.form)]
        placering = []

        # her laver vi en liste der tegner vores brik.
        for y, line in enumerate(format):
            row = list(line)
            for x, column in enumerate(row):
                if column == 'X':
                    placering.append((ny_brik.x + x, ny_brik.y + y))

        # placer brikken paa banen
        for i, pos in enumerate(placering):
            placering[i] = (pos[0] -2, pos[1] -4 )

        # her placerer vi brikken ved hjaelp af en farve
        for i, pos in enumerate(placering):
            x,y = placering[i]
            if y > -1:
                bane[y][x] = ny_brik.farve

        opdater_bane(skaerm,bane)    
    pygame.display.update()

# start spillet
startskaerm()
spillet()

# gameover billede
# lave selve spillets layout
# Lave nogle brikker
# Vi skal kunne flytte rundt paa nogle brikker
# Vi skal have nogle point (ved at fylde en hel raekke)