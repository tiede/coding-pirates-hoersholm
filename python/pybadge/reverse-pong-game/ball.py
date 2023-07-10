from adafruit_display_shapes.circle import Circle
from adafruit_pybadger import pybadger

class Ball:
    def __init__(self, diameter, start_x, start_y, skaerm_hoejde, skaerm_bredde):
        # Gem i variabler
        self.diameter = diameter
        self.x = start_x
        self.y = start_y
        self.start_x = start_x
        self.start_y = start_y
        
        # Lav cirkel
        self.circle = Circle(self.x, self.y, self.diameter, fill=0x00FF00, outline=0xFF00FF)
        
        # default til at bevæge sig mod højre
        self.hoejre = True
        
        # Skærm højde og bredde kan fortælle os om vi bevæger os ud af skærmen
        self.skaerm_hoejde = skaerm_hoejde
        self.skaerm_bredde = skaerm_bredde

        # PyBadger er en klasse der gør det nemt at håndtere knapper
        self.badger = pybadger
        
    def update(self, paddle_venstre, paddle_hoejre):
        print("Inde i ball update")

        # Hvis vi bevæger os mod højre skal vi lægge til x ellers trække fra
        if self.hoejre == True:
            self.x += 1
        else:
            self.x -= 1

        # Få bold til at flytte sig
        # Check for op knap
        if self.badger.button.up > 0:
            # Flyt op
            self.y -= 1
        
        # Check for ned knap
        if self.badger.button.down > 0:
            # move down
            self.y += 1

        # Check om vi rammer paddle
        if self.x == paddle_venstre.x + paddle_venstre.bredde and paddle_venstre.y < self.y < paddle_venstre.y + paddle_venstre.hoejde:
            # Hvis vi rammer venstre paddle så skift retning til at bevæge sig mod højre
            self.hoejre = True
            print("Kollision venstre paddle")
            
        if self.x == paddle_hoejre.x - paddle_hoejre.bredde and paddle_hoejre.y < self.y < paddle_hoejre.y + paddle_hoejre.hoejde:
            # Hvis vi rammer højre paddle så skift retning til at bevæge sig mod venstre
            self.hoejre = False
            print("Kollision højre paddle")        

        # Opdater cirkelens position
        self.circle.x = self.x
        self.circle.y = self.y