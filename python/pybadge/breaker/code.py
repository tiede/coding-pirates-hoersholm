# Vi importerer de standardfunktioner som vi skal bruge i vores spil

import board  # dette er knapperne
import displayio # dette er skærmen
import terminalio # dette giver mulighed for tekst
import time # hvor lang tid er der gået 
import supervisor

from adafruit_pybadger import pybadger
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_text.label import Label

# vi sætter nu skærmens størrelse
# Variablerne herunder står med store bogstaver fordi det er KONSTANTER
# En konstant er en variabel som aldrig ændrer sig i spillet.

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 128

RED = 0xFF0000 
GREEN = 0x00FF00
BLUE = 0x0000FF
YELLOW = 0xFFFF00
WHITE = 0xFFFFFF
BLACK = 0x000000
GREY = 0x808080

FPS = 60
FPS_FORSINKELSE = 1 / FPS

# Der skal lave en række global variabler:
point = 0
highscore = 0 

# Hvis man har en variabel som f.eks. dem herunder hvor det er = [] så betyder det at det er en liste
blok_listeLinje1 = []
blok_listeLinje2 = []
blok_listeLinje3 = []
blok_listeLinje4 = []
blok_listeLinjeAntal1 = []
blok_listeLinjeAntal2 = []
blok_listeLinjeAntal3 = []
blok_listeLinjeAntal4 = []

score_label = Label(terminalio.FONT, text= "Point:", color=WHITE, x=5, y=5)

bredde = 18
hoejde = 8

# Indlæs startknap billede
startbillede = displayio.TileGrid(displayio.OnDiskBitmap(open("/start.bmp", "rb")), pixel_shader=displayio.ColorConverter())
startbillede.x = 10
startbillede.y = 10

# Indlæs game over billede
gameoverbillede = displayio.TileGrid(displayio.OnDiskBitmap(open("/GameOver.bmp", "rb")), pixel_shader=displayio.ColorConverter())
gameoverbillede.x = 1
gameoverbillede.y = 1

def restart_script():
    supervisor.reload()
    # script_filename = "code.py"
    # with open(script_filename, "r") as file:
    #     script_code = file.read()
    #     exec(script_code, globals())

# Vi skal have en funktion som kontrollerer om en bold har ramt en blok
def blok_ramt():
    circle_x1 = bold.x
    circle_x2 = bold.x + bold.diameter
    circle_y1 = bold.y
    circle_y2 = bold.y + bold.diameter

    rectangle_x1 = Blok.x 
    rectangle_x2 = Blok.x + Blok.bredde
    rectangle_y1 = Blok.y
    rectangle_y2 = Blok.y + Blok.hoejde

    ramt_venstre = rectangle_x1 < circle_x2
    ramt_hoejre = rectangle_x2 > circle_x1
    ramt_top = rectangle_y1 < circle_y2
    ramt_bund = rectangle_y2 > circle_y1

    if ramt_venstre and ramt_hoejre and ramt_top and ramt_bund:
        print(Blok.x)
        return True
    return False

def intersect(bold_circle, blok_rect):
    circle_x1 = bold_circle.x
    circle_x2 = bold_circle.x + bold_circle.diameter
    circle_y1 = bold_circle.y
    circle_y2 = bold_circle.y + bold_circle.diameter

    rectangle_x1 = blok_rect.x 
    rectangle_x2 = blok_rect.x + blok_rect.width
    rectangle_y1 = blok_rect.y
    rectangle_y2 = blok_rect.y + blok_rect.height

    ramt_venstre = rectangle_x1 < circle_x2
    ramt_hoejre = rectangle_x2 > circle_x1
    ramt_top = rectangle_y1 < circle_y2
    ramt_bund = rectangle_y2 > circle_y1

    if ramt_venstre and ramt_hoejre and ramt_top and ramt_bund:
        return True
    return False

# Så skal vi lave funktionen til at tegne en blok og et bat

class Blok:
    def __init__(self, bredde, hoejde, pos_x, pos_y, farve):
        # gem i variabler
        self.bredde = bredde
        self.hoejde = hoejde
        self.x = pos_x
        self.y = pos_y
        self.farve = farve

        # så skal vi tegne firkanten
        self.rect = Rect(self.x,self.y,self.bredde,self.hoejde,fill=farve)

    def update(self):
        self.badger = pybadger #Nu har vi adgang til nogle knapper
        if self.badger.button.left > 0 and self.x > 0:
            self.x -= 2

        if self.badger.button.right > 0 and self.x < SCREEN_WIDTH-self.bredde:
            self.x += 2

        # Nu skal vi opdatere den nye placering af vores bat
        self.rect.x = self.x
        self.rect.y = self.y

class Bold:
    def __init__(self,diameter,start_x,start_y):
        self.diameter = diameter
        self.x = start_x
        self.y = start_y
        self.hoejre = True
        self.op = True
        self.start = False
        self.blokramt = False

        # tegn lige en cirkel/bold
        self.circle = Circle(self.x,self.y,self.diameter,fill=RED,outline=YELLOW)

    def ramt_bat(self, blok_listeLinjeAntal, blok_listeLinje):
        for loekke in range(7):
            if len(blok_listeLinjeAntal) > 0:
                
                if intersect(self, blok_listeLinje[loekke]):
                    if loekke in blok_listeLinjeAntal:
                            splash.remove(blok_listeLinje[loekke])
                            blok_listeLinjeAntal.remove(loekke)
                            self.op = False
                            return True
        return False

    def update(self):
        global point
        self.badger = pybadger # Nu har vi adgang til nogle knapper
        self.start = True
        if self.start == True:    
            #Vi er retning mod hoejre
            if self.x == SCREEN_WIDTH-6:
                self.hoejre = False

            #Vi er i retning mod venstre
            if self.x == 0:
                self.hoejre = True

            #Vi er i retning mod toppen
            if self.y == 0:
                self.op = False

            #Vi er i retning mod bunden            
            if self.y == SCREEN_HEIGHT -6:
                self.op = True
    
            #Nu skal vi rette x
            if self.hoejre == True:
                self.x += 1
            else:
                self.x -= 1    

            #Nu skal vi rette y
            if self.op == True:
                self.y -= 1
            else:
                self.y += 1    

            # Vi skal tjekke om vi har ramt en blok - har vi det så skal vi have et point
                # a) Vi kan tjekke om x,y har en farve som er RED, GREEN,BLUE, YELLOW
                # b) vi kan lave et array dvs. en oversigt over alle blokke vi har oprettet og så fjerne en blok 

            if spilstartet == True:
                if self.op == True:
                    #if blok_ramt:
                    ramt4 = self.ramt_bat(blok_listeLinjeAntal4, blok_listeLinje4)
                    ramt3 = self.ramt_bat(blok_listeLinjeAntal3, blok_listeLinje3)
                    ramt2 = self.ramt_bat(blok_listeLinjeAntal2, blok_listeLinje2)
                    ramt1 = self.ramt_bat(blok_listeLinjeAntal1, blok_listeLinje1)
                    
                    if ramt4 or ramt3 or ramt2 or ramt1:
                        point += 1

                        # for loekke in range(7):
                        #     if len(blok_listeLinjeAntal4) > 0:
                        #         if self.y == blok_listeLinje4[loekke].y:
                        #             if blok_listeLinje4[loekke].x <= self.x <= blok_listeLinje4[loekke].x+bredde:
                        #                 if loekke in blok_listeLinjeAntal4:
                        #                     splash.remove(blok_listeLinje4[loekke])
                        #                     blok_listeLinjeAntal4.remove(loekke)
                        #                     point += 1
                        #                     self.op = False
                        #                     #pybadger.play_file('/coin.wav')
                        # for loekke in range(7):
                        #     if len(blok_listeLinjeAntal3) > 0:
                        #         if self.y == blok_listeLinje3[loekke].y:
                        #             if blok_listeLinje3[loekke].x <= self.x <= blok_listeLinje3[loekke].x+bredde:
                        #                 if loekke in blok_listeLinjeAntal3:
                        #                     splash.remove(blok_listeLinje3[loekke])
                        #                     blok_listeLinjeAntal3.remove(loekke)
                        #                     point += 1
                        #                     self.op = False
                        #                     #pybadger.play_file('/coin.wav')                                        
                        # for loekke in range(7):
                        #     if len(blok_listeLinjeAntal2) > 0:
                        #         if self.y == blok_listeLinje2[loekke].y:
                        #             if blok_listeLinje2[loekke].x <= self.x <= blok_listeLinje2[loekke].x+bredde:
                        #                 if loekke in blok_listeLinjeAntal2:
                        #                     splash.remove(blok_listeLinje2[loekke])
                        #                     blok_listeLinjeAntal2.remove(loekke)
                        #                     point += 1
                        #                     self.op = False
                        #                     #pybadger.play_file('/coin.wav')               
                        # for loekke in range(7):
                        #     if len(blok_listeLinjeAntal1) > 0:
                        #         if self.y == blok_listeLinje1[loekke].y:
                        #             if blok_listeLinje1[loekke].x <= self.x <= blok_listeLinje1[loekke].x+bredde:
                        #                 if loekke in blok_listeLinjeAntal1:
                        #                     splash.remove(blok_listeLinje1[loekke])
                        #                     blok_listeLinjeAntal1.remove(loekke)
                        #                     point += 1
                        #                     self.op = False
                        #                     #pybadger.play_file('/coin.wav')               
                    
                    score_label.text = "Point: " + str(point) 

                # Vi skal tjekke om Y = 128og ikke har ramt battet - saa er det game over
                # a) Hvis Y = 128 og positionens farve er = WHITE så har vi ramt battet
                # b) Er den sort = game over.
                if self.op == False:
                    if (intersect(bold, Bat.rect)):
                        self.op = True
                    elif (self.y >= 120):
                        gameover(point)

                    # if self.y == 120:
                    #     if not (Bat.x-2 <= self.x <= Bat.x+bredde+2):              
                    #         gameover(point)
                    #     else:
                    #       self.op = True      

            # til sidst skal vi placere bolden
            self.circle.x = self.x
            self.circle.y = self.y

            #Hvis alle blokke er fjernet så lav nogle nye
            if spilstartet == True:
                if len(blok_listeLinjeAntal1) + len(blok_listeLinjeAntal2) + len(blok_listeLinjeAntal3) + len(blok_listeLinjeAntal4) == 0:
                    splash_copy = list(splash)
                    for child in splash_copy:
                        splash.remove(child) 
                    lavbane()

import random
def lav_raekker(start_x, start_y, farve_liste, start):
    for raekker in range(2): 
        for antal_blokke in range(8):
            tilfaeldigfarve = random.choice(farve_liste)
            tegn_blok = Blok(bredde,hoejde, start_x, start_y, tilfaeldigfarve)
            start.append(tegn_blok.rect)
            start_x += 20
        start_x = 1
        start_y += 10 

def startskaerm():
    # Lav display
    start = displayio.Group() # klargører skærmen
    board.DISPLAY.show(start)
    start.append(startbillede)

    lav_raekker(1, 1, [RED,GREEN,BLUE,YELLOW], start)
    lav_raekker(1, 100, [RED,GREEN,BLUE,YELLOW], start)

    # start_x = 1
    # start_y = 1
    # import random
    # farve_liste = [RED,GREEN,BLUE,YELLOW]
    # for raekker in range(2): 
    #     for antal_blokke in range(8):
    #         tilfaeldigfarve = random.choice(farve_liste)
    #         tegn_blok = Blok(bredde,hoejde, start_x, start_y, tilfaeldigfarve)
    #         start.append(tegn_blok.rect)
    #         start_x += 20
    #     start_x = 1
    #     start_y += 10

    # start_x = 1
    # start_y = 100
    # import random
    # farve_liste = [RED,GREEN,BLUE,YELLOW]
    # for raekker in range(2): 
    #     for antal_blokke in range(8):
    #         tilfaeldigfarve = random.choice(farve_liste)
    #         tegn_blok = Blok(bredde,hoejde, start_x, start_y, tilfaeldigfarve)
    #         start.append(tegn_blok.rect)
    #         start_x += 20
    #     start_x = 1
    #     start_y += 10

    start_bolde = []
    start_bolde.append(Bold(3,5,SCREEN_HEIGHT-30))
    start_bolde.append(Bold(3,40,SCREEN_HEIGHT-95))
    start_bolde.append(Bold(3,55,SCREEN_HEIGHT-50))
    start_bolde.append(Bold(3,60,SCREEN_HEIGHT-12))
    start_bolde.append(Bold(3,105,SCREEN_HEIGHT-70))
    start_bolde.append(Bold(3,120,SCREEN_HEIGHT-110))
    start_bolde.append(Bold(3,155,SCREEN_HEIGHT-80))
    start_bolde.append(Bold(3,80,SCREEN_HEIGHT-33))
    start_bolde.append(Bold(3,20,SCREEN_HEIGHT-10))
    start_bolde.append(Bold(3,160,SCREEN_HEIGHT))

    for bold in start_bolde:
        start.append(bold.circle)
    
    # startbold = Bold(3,5,SCREEN_HEIGHT-30)
    # startbold2 = Bold(3,40,SCREEN_HEIGHT-95)
    # startbold3 = Bold(3,55,SCREEN_HEIGHT-50)
    # startbold4 = Bold(3,60,SCREEN_HEIGHT-12)
    # startbold5 = Bold(3,105,SCREEN_HEIGHT-70)
    # startbold6 = Bold(3,120,SCREEN_HEIGHT-110)
    # startbold7 = Bold(3,155,SCREEN_HEIGHT-80)
    # startbold8 = Bold(3,80,SCREEN_HEIGHT-33)
    # startbold9 = Bold(3,20,SCREEN_HEIGHT-10)
    # startbold10 = Bold(3,160,SCREEN_HEIGHT)
    # start.append(startbold.circle)
    # start.append(startbold2.circle)
    # start.append(startbold3.circle)
    # start.append(startbold4.circle)
    # start.append(startbold5.circle)
    # start.append(startbold6.circle)
    # start.append(startbold7.circle)
    # start.append(startbold8.circle)
    # start.append(startbold9.circle)
    # start.append(startbold10.circle)
    startknap = pybadger

    while not startknap.button.start:
        for bold in start_bolde:
            bold.update()
        # startbold.update()
        # startbold2.update()
        # startbold3.update()
        # startbold4.update()
        # startbold5.update()
        # startbold6.update()
        # startbold7.update()
        # startbold8.update()
        # startbold9.update()
        # startbold10.update()
        time.sleep(0.01)

def gameover(point):
    visgameover = displayio.Group() 
    board.DISPLAY.show(visgameover)
    visgameover.append(gameoverbillede)
    gameover_label = Label(terminalio.FONT, text= "Flot du fik "+str(point)+" Point.", color=BLACK, x=10, y=60)
    gameover_label.anchor_point = (1,0) 
    visgameover.append(gameover_label)
    gameoverknap = pybadger

    while not gameoverknap.button.start:
        time.sleep(0.01)
    restart_script()
        
def lavbane():   
    # Lav display
    global splash
    splash = displayio.Group() # klargører skærmen
    board.DISPLAY.show(splash)
    
    # Lave baggrunden i spillet
    color_bitmap = displayio.Bitmap(SCREEN_WIDTH,SCREEN_HEIGHT,2)

    color_palette = displayio.Palette(1)
    # når der står noget med hårde / kantede paranteser så kaldes de ofte for et ARRAY
    color_palette[0] = BLACK 

    bg_sprite = displayio.TileGrid(color_bitmap,pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)

    # tegn vore point/score
    #score_label = Label(terminalio.FONT, text= "Point:", color=WHITE, x=5, y=5)
    score_label.anchor_point = (1,0) 
    splash.append(score_label)

    # tegn en række af kasser
    bredde = 18
    hoejde = 8
    start_x = 12
    start_y = 12

    for loekke in range(7):
        tegn_blok = Blok(bredde,hoejde, start_x, start_y, RED)
        blok_listeLinje1.append(tegn_blok.rect)
        blok_listeLinjeAntal1.append(loekke) 
        start_y += 10
        
        tegn_blok = Blok(bredde,hoejde, start_x, start_y, GREEN)
        blok_listeLinje2.append(tegn_blok.rect)
        blok_listeLinjeAntal2.append(loekke)
        start_y += 10

        tegn_blok = Blok(bredde,hoejde, start_x, start_y, BLUE)
        blok_listeLinje3.append(tegn_blok.rect)
        blok_listeLinjeAntal3.append(loekke)
        start_y += 10

        tegn_blok = Blok(bredde,hoejde, start_x, start_y, YELLOW)
        blok_listeLinje4.append(tegn_blok.rect)
        blok_listeLinjeAntal4.append(loekke) 

        start_x += 20 # Da bredden er 18 på en blok så laver vi 2 pixels som mellemrum
        start_y = 12

    for loekke in range(7):
        splash.append(blok_listeLinje1[loekke])
        splash.append(blok_listeLinje2[loekke])
        splash.append(blok_listeLinje3[loekke])
        splash.append(blok_listeLinje4[loekke])

    # Det her er den gamle kode
    #farve_liste = [RED,GREEN,BLUE,YELLO0W] 
    #for farvesjov in farve_liste: 
    #    for antal_blokke in range(7):
    #        tegn_blok = Blok(bredde,hoejde, start_x, start_y, farvesjov)
    #        splash.append(tegn_blok.rect)
    #        start_x += 20        
    #    start_x = 12
    #    start_y += 10

    # Tegne et bat
    global Bat
    Bat = Blok(22,6,int(SCREEN_WIDTH/2)-11,int(SCREEN_HEIGHT-8),WHITE)
    splash.append(Bat.rect)

    # Tegne en bold
    global bold
    bold = Bold(3,int(SCREEN_WIDTH/2),SCREEN_HEIGHT-12)
    splash.append(bold.circle)

spilstartet = False
startskaerm()
spilstartet = True
lavbane()

sidst_opdateret = 0
tid = 0

# og så starter vi spillet 
while True:
    tid = time.monotonic()
    if sidst_opdateret + FPS_FORSINKELSE <= tid:
        Bat.update()
        bold.update()
        sidst_opdateret = tid