import pygame
import random

pygame.init()

# Højde og bredde for spillet
højde = 300
bredde = 800

FPS = 30
FramePerSec = pygame.time.Clock()

#Så bestemmer vi størrelsen på skærmen/vinduet som spillet skal køre i.
skærm = pygame.display.set_mode((bredde,højde))

# Billeder som skal bruges i spillet
jord_billede = pygame.image.load("jord.png")
dino_billede = pygame.image.load("dinoer.png")
dino_duk_billede = pygame.image.load("dinoduk.png")
kaktus_billede = pygame.image.load("kaktus.png")
fugl_billede = pygame.image.load("fugl.png")

hoppe_lyd = pygame.mixer.Sound("hop.wav")
highscore_fil = 'highscore.txt'

# Vi skal læse highscoren i vores highscore fil
with open(highscore_fil,'r') as fil:
    highscore = int(fil.read(),2) # vi læser highscoren fra filen binært
    fil.close()

# Vi gemmre lige den hichscore som vi har læst fra filen
gammel_highscore = highscore

# når der står -10 så er det højden på jorden.
dino = {'x': 100, 'y':højde-95-10,'bredde':440/5, 'højde':95, 'billede_nr':2,'hopper':False, 'y_min': højde-95,'opad': True,'dukker':False}
dino_duk = {'x': 100, 'y' : højde - 61, 'bredde' : 236/2, 'højde': 61, 'billede_nr': 0}
fugl = {'x': bredde-80, 'y': højde-150-10, 'bredde':184/2, 'højde':81,'billede_nr':1}
kaktus = {'x': bredde-34, 'y':højde-70-13,'bredde':206/6, 'højde':70, 'billede_nr':2}
jord = {'x1':0, 'x2':1203, 'y': højde-19, 'bredde': 1203}

antalpoint = 0
erdettidtilenkaktus = False
erdettidtilenfugl = False
kør = True

def setup():
    global antalpoint, erdettidtilenkaktus, erdettidtilenfugl, kør
    global dino, fugl, kaktus, jord
    antalpoint = 0
    erdettidtilenfugl = False
    erdettidtilenkaktus = False
    kør = True
    dino = {'x': 100, 'y':højde-95-10,'bredde':440/5, 'højde':95, 'billede_nr':2,'hopper':False, 'y_min': højde-95,'opad': True,'dukker':False}
    fugl = {'x': bredde-80, 'y': højde-140-10, 'bredde':184/2, 'højde':81,'billede_nr':1}
    kaktus = {'x': bredde-34, 'y':højde-70-13,'bredde':204/6, 'højde':70, 'billede_nr':2}
    jord = {'x1':0, 'x2':1203, 'y': højde-19, 'bredde': 1203}

def dino_hopper():
    if dino['opad']:
        dino['y'] -= 8
    else:
        dino['y'] += 10

    # Vi bliver ved med at bevæge os opad indtil vi når en højde på 100 eller lavere og så skal vi gå nedad.
    if dino['y'] < 30:
        dino['opad'] = False    

    # når vi igen når jorden så skal vi ikke længere hoppe
    if dino['y'] > 195:
        dino['hopper'] = False
        dino['opad'] = True
        # Vi skal selvfølgelig lande lige præcist på jorden hverken over/under
        dino['y'] = højde-dino['højde']-10

def dino_dukker():
    pass

class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def right(self):
        return self.x + self.width
    
    def bottom(self):
        return self.y + self.height

def dino_ramt(A: Rectangle, B: Rectangle) -> bool:
    return not (A.right() <= B.x or  
                B.right() <= A.x or  
                A.bottom() <= B.y or  
                B.bottom() <= A.y)

def gameOver():
    skrifttype1 = pygame.font.SysFont("Arial",80,True)
    skrifttype2 = pygame.font.SysFont("Arial",36,True)
    gameover_tekst = skrifttype1.render('Game Over!!',True, (255,0,255))
    trykpaaenknap_tekst = skrifttype2.render('Tryk på en tast for at prøve igen', True, (0,0,0))
    skærm.blit(gameover_tekst,(160,100))
    skærm.blit(trykpaaenknap_tekst, (140,200))
    pygame.display.flip()
    
    # Hvis den nye highscore er højere end den gamle så skal vi gemme den nye highscore
    if highscore > gammel_highscore:
        with open(highscore_fil,'w') as fil:
            fil.write(str(bin(highscore))) # tilføj bin( ) for at gemme highscoren binært
        
    trykpaaenknap = True
    while trykpaaenknap:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                trykpaaenknap = False
    setup()

while kør:

    skærm.fill((255,255,255))
    skærm.blit(jord_billede,(jord['x1'],jord['y']))
    skærm.blit(jord_billede,(jord['x2'],jord['y']))
    
    skrifttype = pygame.font.SysFont("Arial",20,True)
    score_tekst = skrifttype.render('Highscore: '+str(highscore)+' Score: '+str(antalpoint),True, (255,0,0))
    skærm.blit(score_tekst,(10,10))

    quit = False
    # Der skal ske noget når man trykker på en knap
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #kør = False
            quit = True
        if event.type == pygame.KEYDOWN:
            #Der blev trykket på en knap - hvilken knap var det så??
            if event.key == pygame.K_ESCAPE:
                #kør = False
                quit = True
            if event.key == pygame.K_SPACE:
                dino['hopper'] = True
                dino['dukker'] = False
                dino_hopper()
            if event.key == pygame.K_UP:
                dino['hopper'] = True
                dino['dukker'] = False
                dino_hopper()
            if event.key == pygame.K_DOWN:  
                dino['hopper'] = False
                dino['dukker'] = True
                dino_dukker()
 
    if dino['billede_nr'] >= 3:
        dino['billede_nr'] = 0
    else:
        dino['billede_nr']+= 1    

    if dino['hopper']:
        dino_hopper()

    if dino['dukker']:
        print('Dinoen dukker')
        if (dino_duk['billede_nr'] == 1):
            dino_duk['billede_nr'] = 0
        else:
            dino_duk['billede_nr'] = 1

    if fugl['billede_nr'] == 1:
        fugl['billede_nr'] = 0
    else:
        fugl['billede_nr'] = 1    

    if (dino['dukker']):
        skærm.blit(dino_duk_billede,(dino_duk['x'],dino_duk['y']),
                (dino_duk['bredde']*int(dino_duk['billede_nr']),0,dino_duk['bredde'],dino_duk['højde']))    
    else:
        skærm.blit(dino_billede,(dino['x'],dino['y']),
                (dino['bredde']*int(dino['billede_nr']),0,dino['bredde'],dino['højde']))    

    fugl_venstre = fugl['bredde']*fugl['billede_nr']
    fugl_top = 0
    fugl_bredde = fugl['bredde']
    fugl_hojde = fugl['højde']
    skærm.blit(fugl_billede,(fugl['x'],fugl['y']),(fugl_venstre,fugl_top,fugl_bredde,fugl_hojde))

    # Lad os tilføje en kaktus til spillet
    if antalpoint % 150 == 0:
       erdettidtilenkaktus = True 
       kaktus['x'] = bredde-34

    if erdettidtilenkaktus == True:
        skærm.blit(kaktus_billede,(kaktus['x'],kaktus['y']),(kaktus['billede_nr'],0,kaktus['bredde'],kaktus['højde']))
        # erdettidtilenkaktus = False
    
    # Lad os tilføje en fugl til spillet
    if antalpoint % 200 == 0:
        erdettidtilenfugl = True
        fugl['x'] = bredde-80

    if erdettidtilenfugl == True:
        skærm.blit(fugl_billede,(fugl['x'],fugl['y']),(fugl['bredde']*fugl['billede_nr'],0,fugl['bredde'],fugl['højde']))
    
    if (dino['dukker']):
        dino_position = Rectangle(dino_duk['x'] + 10, dino_duk['y'], dino_duk['bredde'] - 10, dino_duk['højde'])
    else:
        dino_position = Rectangle(dino['x'] + 10, dino['y'], dino['bredde'] - 10, dino['højde'])
    
    kaktus_position = Rectangle(kaktus['x'], kaktus['y'], kaktus['bredde'], kaktus['højde'])
    fugl_position = Rectangle(fugl['x'], fugl['y'], fugl['bredde'], fugl['højde'])

    if dino_ramt(dino_position, fugl_position):
        print('Dinoen har ramt fuglen')
        kør = False
    if dino_ramt(dino_position, kaktus_position):
        print('Dinoen har ramt kaktus')
        kør = False
        
    #Lad os få fuglen til at flytte sig
    fugl['x'] -= 20

    if fugl['x'] < -fugl['bredde']:
        pass

    # Lad os få kaktussen til at flytte sig
    kaktus['x'] -= 10
    if kaktus['x'] < -kaktus['bredde']:
        pass

    # Lad os få jorden til at flytte sig
    jord['x1'] -= 10
    jord['x2'] = jord['bredde'] + jord['x1']
    if jord['x1'] * -1 >=  jord['bredde']:
        jord['x1'] = 0

    # vi skal have nogle point
    antalpoint += 2
    
    # Hvis point er højere end highscore så opdater highscoren
    if antalpoint > highscore:
        highscore = antalpoint
            
    # Hvis Kør = false så er det slut
    if kør == False:
        gameOver()

    if quit == True:
        pygame.quit()

    # Vi opdaterer lige skærmbilledet    
    pygame.display.flip()

    #pygame.time.delay(40)
    FramePerSec.tick(FPS)

    if (antalpoint % 100 == 0):
        FPS = FPS + 2