from machine import Pin
import time

led = Pin(2, Pin.OUT)
knap = Pin(15, Pin.IN)

knap_nede = time.ticks_ms()
knap_oppe = time.ticks_ms()

forrige_knap_vaerdi = 0
while(True):
    knap_vaerdi = knap.value()
    
    led.value(not knap_vaerdi)
    
    # Hvis knap trykket ned
    if (knap_vaerdi == 0 and forrige_knap_vaerdi == 1):
        print('Knap ned')
        knap_nede = time.ticks_ms()
        forrige_knap_vaerdi = 0
    elif (knap_vaerdi == 1 and forrige_knap_vaerdi == 0):
        print('Knap op')
        knap_oppe = time.ticks_ms()
        forrige_knap_vaerdi = 1
    time.sleep(0.1)