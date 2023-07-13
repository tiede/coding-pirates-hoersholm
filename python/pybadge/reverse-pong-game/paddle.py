from adafruit_display_shapes.rect import Rect
from adafruit_pybadger import pybadger

class Paddle:
    def __init__(self, bredde, hoejde, start_x, start_y, skaerm_hoejde):
        # Gem i variabler
        self.hoejde = hoejde
        self.bredde = bredde
        self.x = start_x
        self.y = start_y

        self.y = int(skaerm_hoejde/2 - hoejde / 2)

        # Lav en firkant
        self.rect = Rect(self.x, self.y, self.bredde, self.hoejde, fill=0x0)
        
        # Defalut til at bevæge sig op
        self.opad = True
        
        # Højde på skærmen så den ved hvornår vi skal skifte retning
        self.skaerm_hoejde = skaerm_hoejde

        self.badger = pybadger
        
    def update(self):
        #print("inside paddle update")
        
        # Check for op knap
        if self.badger.button.up > 0 and self.y > 0:
            # Flyt op
            self.y -= 1
        
        # Check for ned knap
        if self.badger.button.down > 0 and self.y < self.skaerm_hoejde - self.hoejde:
            # move down
            self.y += 1
            
        # Hvis vi rammer toppen eller bunden, så skift retning
        if self.y <= 0:
            self.opad = False
        if self.y >= self.skaerm_hoejde - self.hoejde:
            self.opad = True
        
        # Opdater firkantens position
        self.rect.x = self.x
        self.rect.y = self.y