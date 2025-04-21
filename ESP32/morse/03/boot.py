from machine import Pin
from machine import Timer
import time
import morse

led = Pin(2, Pin.OUT)
ir_led = Pin(4, Pin.OUT)
switch = Pin(15, Pin.IN, Pin.PULL_UP)

BASE_TIME_SECONDS = 0.5
TOLERANCE = BASE_TIME_SECONDS / 2.0

sequence = ''
letters = []
words = []

def metronome(timer):
    led.value(not led.value())

metronome_timer = Timer(1)
metronome_timer.init(period=int((BASE_TIME_SECONDS*1000)/2), callback=metronome)

def emit_morse_unit(unit):
    print(unit)
    ir_led.value(1)
    if unit == '.':
        time.sleep(BASE_TIME_SECONDS)
    elif unit == '-':
        time.sleep(3 * BASE_TIME_SECONDS)
    ir_led.value(0)
    time.sleep(BASE_TIME_SECONDS)

print('started')

ir_led.value(0)
message = 'Hello'.upper()
for char in message:
    morse_code_for_char = morse.get_by_char(char)
    if morse_code_for_char != None:
        print('<NEW_SYMBOL> - ' + char)
        for unit in morse_code_for_char:
            emit_morse_unit(unit)        
        time.sleep(BASE_TIME_SECONDS)
    else:
        print('<SPACE>')
        time.sleep(7*BASE_TIME_SECONDS)