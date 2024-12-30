
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
jord = {'x1': 0, 'x2': 1203, 'y': hojde-19, 'bredde': 1203}

# Tegne dino
dino = {'x': 100, 'y':hojde - 95 - 10, 'bredde': 440/5, 'hojde': 95, 'billede_nr': 1}

# Tegn hvid skærm
skaerm.fill((255,255,255))

FPS = 20
FramePerSec = pygame.time.Clock()

font = pygame.font.SysFont(None, 60)

kor = True
counter = 0

while kor:  
    
    skaerm.blit(billede_jord, (jord['x1'], jord['y']))

    dino_left = dino['bredde']*int(dino['billede_nr'] - 1)
    dino_top = 0
    dino_width = dino['bredde']
    dino_height = dino['hojde']
    dino_rect = (dino_left, dino_top, dino_width, dino_height)
    skaerm.blit(billede_dino, (dino['x'], dino['y']), dino_rect) 
    
    #skaerm.fill((255,255,255))  
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            pass
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.K_SPACE:
            pass
        if event.type == pygame.KEYUP:
            pass
    
    if (dino['billede_nr'] >= 4):
        dino['billede_nr'] = 1
    else:
        dino['billede_nr'] += 1
        
    pygame.display.flip()
    FramePerSec.tick(FPS)