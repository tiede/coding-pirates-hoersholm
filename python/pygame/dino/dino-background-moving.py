
import pygame
import random
from pygame.locals import *
import sys

pygame.init()

hojde = 300
bredde = 800

skaerm = pygame.display.set_mode((bredde, hojde))

billede_jord = pygame.image.load("jord.png")
billede_dino = pygame.image.load("dinoer.png")
billede_dino_duk = pygame.image.load("dinoduk.png")
billede_kaktus = pygame.image.load("kaktus.png")
billede_fugl = pygame.image.load("fugl.png")

hoppe_lyd = pygame.mixer.Sound("hop.wav")

# Tegne jorden
jord1 = {'x1': 0, 'x2': 1203, 'y': hojde-19, 'bredde': 1203}
jord2 = {'x1': 1203, 'x2': 1203 + 1203, 'y': hojde-19, 'bredde': 1203}

# Tegne dino
dino = {'x': 100, 
    'y':hojde - 95 - 10, 
    'bredde': 440/5, 
    'hojde': 95, 
    'billede_nr': 1, 
    'hopper': False,
    'y_min': hojde-95,
    'opad': True,
    'dukker': False}

fugl = {'x': bredde - 92,
    'y': 0,
    'bredde': 184/2, 
    'hojde': 81,
    'billede_nr': 1}

# Tegn hvid skærm
skaerm.fill((255,255,255))

FPS = 20
FramePerSec = pygame.time.Clock()

font = pygame.font.SysFont(None, 60)

kor = True
counter = 0

def dino_hopper():
    if dino['opad']:
        dino['y'] -= 10
        if dino['y'] <= hojde - 95-10-95:
            dino['opad'] = False
    else:
        dino['y'] += 10
        if dino['y'] >= hojde - 95 - 10:
            # Nulstiller dinos y placering
            dino['y'] = hojde - 95 - 10
            dino['hopper'] = False
            dino['opad'] = True

def dino_dukker():
    pass

while kor:  
    # Rens skærm
    skaerm.fill((255,255,255))
    skaerm.blit(billede_jord, (jord1['x1'], jord1['y']))
    skaerm.blit(billede_jord, (jord2['x1'], jord2['y']))

    jord1['x1'] -= 16
    jord2['x1'] -= 16

    if (jord1['x1'] + 1203 <= 0):
        print('flyt jord1')
        jord1['x1'] = jord2['x1'] + 1203
    if (jord2['x1'] + 1203 <= 0):
        print('flyt jord2')
        jord2['x1'] = jord1['x1'] + 1203    
      
    # lav point og hi-score
    font = pygame.font.SysFont('Arial', 20)
    score_txt = 'Highscore ' + str(100) + ' Score ' + str(0) 
    score_rendered = font.render(score_txt, True, (0,0,0))
    skaerm.blit(score_rendered, (bredde - (score_rendered.get_width() + 10), 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                dino['hopper'] = True
                print('hop')
            if event.key == pygame.K_DOWN:
                print('duk')
                dino_dukker()
    
    if dino['hopper']:
        dino_hopper()

    if (dino['billede_nr'] >= 3):
        dino['billede_nr'] = 1
    else:
        dino['billede_nr'] += 1
        
    dino_left = dino['bredde']*int(dino['billede_nr'])
    dino_top = 0
    dino_width = dino['bredde']
    dino_height = dino['hojde']
    dino_rect = (dino_left, dino_top, dino_width, dino_height)
    
    skaerm.blit(billede_dino, (dino['x'], dino['y']), dino_rect)

    if (fugl['billede_nr'] == 0):
        fugl['billede_nr'] = 1
    else:
        fugl['billede_nr'] = 0

    fugl_left = fugl['bredde']*int(fugl['billede_nr'])
    fugl_top = 0
    fugl_width = fugl['bredde']
    fugl_height = fugl['hojde']
    fugl_rect = (fugl_left, fugl_top, fugl_width, fugl_height)
    skaerm.blit(billede_fugl, (fugl['x'], fugl['y']), fugl_rect) 

    pygame.display.flip()
    FramePerSec.tick(FPS)