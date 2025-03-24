from machine import Pin
from time import sleep

led = Pin(2, Pin.OUT)                    # D2 - led control
switch = Pin(15, Pin.IN, Pin.PULL_UP)       # D4 - switch input

while True:
    if switch.value() == 0:                # Switch is pressed
        led.value(1)                     # Turn on led
    else:
        led.value(0)                     # Turn off led
    sleep(0.05)                            # Small delay to debounce


