from machine import Pin
import time
import morse as morse

DOT_TID = 0.5

led = Pin(2, Pin.OUT)
knap = Pin(15, Pin.IN)

knap_nede = time.ticks_ms()
knap_oppe = time.ticks_ms()

sekvens = ''

forrige_knap_vaerdi = 0
while(True):
    knap_vaerdi = knap.value()
    
    led.value(not knap_vaerdi)
    
    # Hvis knap trykket ned
    if (knap_vaerdi == 0 and forrige_knap_vaerdi == 1):
        print('Knap ned')
        knap_nede = time.ticks_ms()
        
        delta = (knap_nede - knap_oppe) / 1000
        if (delta >= DOT_TID * 2.5):
            bogstav = morse.symbols.get(sekvens, '')
            if (bogstav != ''):
                print ('Nyt bogstav ' + bogstav)
            else:
                print(str(delta) + ' : Kan ikke afkode sekvens')
            sekvens = ''
        
        forrige_knap_vaerdi = 0
    elif (knap_vaerdi == 1 and forrige_knap_vaerdi == 0):
        print('Knap op')
        knap_oppe = time.ticks_ms()
        
        delta = (knap_oppe - knap_nede) / 1000
        
        # Vi skal finde ud af hvor lang tid knappen har været trykket ned
        if (delta >= DOT_TID * 0.5 and delta <= DOT_TID * 1.5):
            sekvens += '.'
        elif (delta >= DOT_TID * 2.5 and delta <= DOT_TID * 3.5):
            sekvens += '-'
        else:
            print(str(delta) + " : Kan ikke afkode symbol ud fra tid")
            
        print('Sekvens ' + sekvens)
        
        forrige_knap_vaerdi = 1
    time.sleep(0.1)
