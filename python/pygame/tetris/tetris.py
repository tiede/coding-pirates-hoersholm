import pygame

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

pygame.init()
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

clock = pygame.time.Clock()

def show_start_screen():
    screen.fill(ORANGE)
    font = pygame.font.SysFont('Comic Sans', 80, bold=True)
    label = font.render('Tryk på en tast', 1, WHITE)
    screen.blit(label, (50,80))

    font = pygame.font.SysFont('Comic Sans', 60, bold=True)
    label = font.render('For at starte spillet', 1, WHITE)
    rect = label.get_bounding_rect()
    screen.blit(label, (rect.centerx, 200))
    
    running = True
    while(running):
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                running = False
        dt = clock.tick(60) / 1000
        pygame.display.update()

    # When we exit the user must have pressed a button

def start_game():
    pass

show_start_screen()
start_game()


pygame.quit()
print ('Exited')