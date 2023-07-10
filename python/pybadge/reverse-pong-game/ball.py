from adafruit_display_shapes.circle import Circle
from adafruit_pybadger import pybadger

class Ball:
    def __init__(self, diameter, start_x, start_y, skaerm_hoejde, skaerm_bredde):
        # Gem i variabler
        self.score = 0
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
        
    def update(self, paddle_venstre, paddle_hoejre, score_label):
        print("Inde i ball update")

        # Hvis vi bevæger os mod højre skal vi lægge til x ellers trække fra
        if self.hoejre == True:
            self.x += 1
        else:
            self.x -= 1

        # Få bold til at flytte sig
        # Check for op knap
        if self.badger.button.up > 0 and self.y > 0:
            # Flyt op
            self.y -= 1
        
        # Check for ned knap
        if self.badger.button.down > 0 and self.y < self.skaerm_hoejde - (self.diameter+1)*2:
            # move down
            self.y += 1

        # Check om vi rammer paddle
        if self.x == paddle_venstre.x + paddle_venstre.bredde and paddle_venstre.y < self.y < paddle_venstre.y + paddle_venstre.hoejde:
            # Hvis vi rammer venstre paddle så skift retning til at bevæge sig mod højre
            self.hoejre = True
            self.score = self.score + 1
            print("Kollision venstre paddle")
            
        if self.x == paddle_hoejre.x - paddle_hoejre.bredde and paddle_hoejre.y < self.y < paddle_hoejre.y + paddle_hoejre.hoejde:
            # Hvis vi rammer højre paddle så skift retning til at bevæge sig mod venstre
            self.hoejre = False
            self.score = self.score + 1
            print("Kollision højre paddle")

        # Start forfra hvis vi rammer venstre eller højre kant
        if self.x <= 0:
            self.x = self.start_x
            self.y = self.start_y
            self.score = 0
        if self.x >= self.skaerm_bredde- self.diameter:
            self.x = self.start_x
            self.y = self.start_y
            self.score = 0

        # Opdater cirkelens position
        self.circle.x = self.x
        self.circle.y = self.y

        # Opdater score
        score_label.text = str(self.score)