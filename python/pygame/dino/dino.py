
import pygame
import random

pygame.init()

height = 300
width = 800

screen = pygame.display.set_mode((width, height))

img_jord = pygame.image.load("jord.png")
img_dino = pygame.image.load("dinoer.png")
img_dino_duk = pygame.image.load("dinoduk.png")
img_kaktus = pygame.image.load("kaktus.png")
img_fugl = pygame.image.load("fugl.png")

sound_hop = pygame.mixer.Sound("hop.wav")