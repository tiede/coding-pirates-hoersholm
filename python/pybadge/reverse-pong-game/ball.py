from adafruit_display_shapes.circle import Circle
from adafruit_pybadger import pybadger

class Ball:
    def __init__(self, diameter, start_x, start_y, skaerm_hoejde, skaerm_bredde):
        # Gem i variabler
        #self.score = 0
        self.diameter = diameter
        self.x = start_x
        self.y = start_y
        self.start_x = start_x
        self.start_y = start_y
        
        # Lav cirkel
        self.circle = Circle(self.x, self.y, self.diameter, fill=0x00FF00, outline=0xFF00FF)
                
        # Skærm højde og bredde kan fortælle os om vi bevæger os ud af skærmen
        self.skaerm_hoejde = skaerm_hoejde
        self.skaerm_bredde = skaerm_bredde

        # PyBadger er en klasse der gør det nemt at håndtere knapper
        self.badger = pybadger

        self.retning_x_y = [1, 1]

    def update(self, paddle_hoejre, faaet_point, game_over):
        # print("Inde i ball update")

        # Start forfra hvis vi rammer højre kant
        if self.x >= self.skaerm_bredde:
            self.x = self.start_x
            self.y = self.start_y
            game_over()

        # Check om vi rammer paddle            
        if self.x + self.diameter >= paddle_hoejre.x and paddle_hoejre.y < self.y + self.diameter < paddle_hoejre.y + paddle_hoejre.hoejde:
            # Hvis vi rammer højre paddle så skift retning til at bevæge sig mod venstre
            self.retning_x_y[0] = - self.retning_x_y[0]
            faaet_point()
            print("Kollision højre paddle")

        # Returner bolden hvis vi rammer venstre
        if self.x <= 0:
            self.retning_x_y[0] = - self.retning_x_y[0]
            self.hoejre = True
            print("Kollision venstre kant")

        # top 
        if self.y <= 0:
            self.retning_x_y[1] = - self.retning_x_y[1]
            print("Kollision top")

        # eller bund
        if self.y >= self.skaerm_hoejde - self.diameter:
            self.retning_x_y[1] = - self.retning_x_y[1]
            print("Kollision bund")

        self.x += self.retning_x_y[0]
        self.y += self.retning_x_y[1]

        # Opdater cirkelens position
        self.circle.x = self.x
        self.circle.y = self.y