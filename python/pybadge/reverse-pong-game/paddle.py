from adafruit_display_shapes.rect import Rect

class Paddle:
    def __init__(self, bredde, hoejde, start_x, start_y, skaerm_hoejde):
        # Gem i variabler
        self.hoejde = hoejde
        self.bredde = bredde
        self.x = start_x
        self.y = start_y
        
        # Lav en firkant
        self.rect = Rect(self.x, self.y, self.bredde, self.hoejde, fill=0x0)
        
        # Defalut til at bevæge sig op
        self.opad = True
        
        # Højde på skærmen så den ved hvornår vi skal skifte retning
        self.skaerm_hoejde = skaerm_hoejde
        
    def update(self):
        #print("inside paddle update")
        
        # Hvis vi kører opad, så skal vi lægge til y ellers trække fra
        if self.opad == True:
            self.y -= 1
        else:
            self.y += 1
            
        # Hvis vi rammer toppen eller bunden, så skift retning
        if self.y <= 0:
            self.opad = False
        if self.y >= self.skaerm_hoejde - self.hoejde:
            self.opad = True
        
        # Opdater firkantens position
        self.rect.x = self.x
        self.rect.y = self.y