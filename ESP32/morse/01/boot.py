from machine import Pin
from machine import Timer
import time
import morse as morse

led = Pin(4, Pin.OUT)
metronome_led = Pin(2, Pin.OUT)
knap_pin = Pin(15, Pin.IN, Pin.PULL_UP)

DOT_TID = 0.5
TOLERANCE = DOT_TID / 2.0

knap_nede = time.ticks_ms()
knap_oppe = time.ticks_ms()

sekvens = ''
letters = []
words = []

def metronome(timer):
    metronome_led.value(not metronome_led.value())

metronome_timer = Timer(1)
metronome_timer.init(period=int((DOT_TID*1000)/2), callback=metronome)

forrige_vaerdi = 0
while True:
    if knap_pin.value() == 0 and forrige_vaerdi == 1:
        print('Knap nede')
        knap_nede = time.ticks_ms()

        led.value(1)

        # Hvor lang tid siden er det siden vi sidst har modtaget signal i sekunder?
        delta = (knap_nede - knap_oppe) / 1000

        # Hvis sidste signal er mellem 2,5*DOT tid og 3.5*DOT tid så er der kommet et nyt bogstav
        if (delta >= DOT_TID * 2.5): # and delta <= DOT_TID * 3.5):
            bogstav = morse.symbols.get(sekvens, '')
            if (bogstav != ''):
                print('Nyt bogstav : ' + bogstav)
            else:
                print(str(delta) + " : Kan ikke afkode sekvensen!")
            sekvens = ''

        forrige_vaerdi = 0
    elif knap_pin.value() == 1 and forrige_vaerdi == 0:
        print('Knap oppe')
        knap_oppe = time.ticks_ms()
        
        led.value(0)
        
        delta = (knap_oppe - knap_nede) / 1000

        # Vi må finde ud af hvor lang tid knappen har været trykket ned
        # Hvis kort tryk
        if (delta >= DOT_TID*0.5 and delta <= DOT_TID*1.5):
            sekvens += '.'
        # Ellers hvis langt tryk
        elif (delta >= DOT_TID*2.5 and delta <= DOT_TID*3.5):
            sekvens += '-'
        else:
            print(str(delta) + " : Kan ikke afkode symbolet ud fra tiden!")

        print('Sekvens : ' + sekvens)

        forrige_vaerdi = 1
