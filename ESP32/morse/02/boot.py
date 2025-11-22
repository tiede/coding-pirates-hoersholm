from machine import Pin
from machine import Timer
import time
#import threading
import morse as morse

led = Pin(2, Pin.OUT)
switch = Pin(15, Pin.IN, Pin.PULL_UP)

BASE_TIME_SECONDS = 0.5
TOLERANCE = BASE_TIME_SECONDS / 2.0

press = time.ticks_ms()
release = time.ticks_ms()

sequence = ''
letters = []
words = []

def metronome(timer):
    led.value(not led.value())

metronome_timer = Timer(1)
metronome_timer.init(period=int((BASE_TIME_SECONDS*1000)/2), callback=metronome)

# Detect whether most recent button press is start of new letter or word
def detect_termination():
    global sequence, release, press
 
    if sequence == '':
        return
 
    delta = calc_delta_in_sec(release, press)
 
    # Check for start of new letter (gap equal to 3 dots)
    if (delta >= ((BASE_TIME_SECONDS * 3) - TOLERANCE)) and (delta <= ((BASE_TIME_SECONDS * 4) + TOLERANCE)):
        process_letter()
 
    # Check for start of new word (gap equal to 7 dots - but assume anything > 7 dots is valid too)
    elif delta >= ((BASE_TIME_SECONDS * 7) - TOLERANCE):
        process_word()
 
    # If it's not a new letter or word, and it's a gap greater than a single dot, tell the user
    elif delta > (BASE_TIME_SECONDS + TOLERANCE):
        print("")
 
# Process letter
def process_letter():
    global sequence
    character = morse.symbols.get(sequence, '')
 
    if character != '':
        print("Interpreted sequence " + sequence + " as the letter: " + character)
        letters.append(character)
        sequence = ""
        return True
    else:
        print('Invalid sequence: ' + sequence + " (deleting current sequence)")
        sequence = ""
        return False
 
# Process word
def process_word():
    if process_letter():
        word = ''.join(letters)
        letters[:] = []
        if word == "AR":
            print("End of transmission. Here's your message: " + ' '.join(words))
            print('\nClearing previous transmission. Start a new one now...\n')
            words[:] = []
        else:
            words.append(word)
 
# Interpret button click (press/release) as dot, dash or unrecognized
def interpret_input():
    global sequence, press, release
 
    delta = calc_delta_in_sec(press, release)
 
    if (delta >= (BASE_TIME_SECONDS - TOLERANCE)) and (delta <= (BASE_TIME_SECONDS + TOLERANCE)):
        sequence += '.'
        print(str(delta) + " : Added dot to sequence:  " + sequence)
    elif (delta >= ((BASE_TIME_SECONDS * 3) - TOLERANCE)) and (delta <= ((BASE_TIME_SECONDS * 3) + TOLERANCE)):
        sequence += '-'
        print(str(delta) + " : Added dash to sequence: " + sequence)
    else:
        print(str(delta) + " : Unrecognized input!")
 
def calc_delta_in_sec(time1, time2):
    delta = (time2 - time1) / 1000
    return delta # + (delta.microseconds / 1000000.0)

print('started')
formerValue = 0
while True:
    if switch.value() == 0 and formerValue == 1:
        time.sleep(0.1)
        if (switch.value() ==0):
            #print('pressed')
            press = time.ticks_ms() 
            formerValue = 0
            detect_termination()
    elif switch.value() == 1 and formerValue == 0:
        time.sleep(0.1)
        if switch.value() == 1: 
            #print('released')
            release = time.ticks_ms()
            formerValue = 1
            interpret_input()