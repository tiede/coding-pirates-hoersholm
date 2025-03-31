from machine import Pin, Timer
import time

# --- LED Pins ---
# Initialiser tre LED'er som udgange: GPIO 2, 15 og 4
leds = [Pin(pin, Pin.OUT) for pin in [2, 15, 4]]

# --- Motorer og knap ---
# Motorstyring: hver motor har to retninger (frem og tilbage)
# Venstre motor: frem = GPIO 18, tilbage = GPIO 22
# Højre motor: frem = GPIO 19, tilbage = GPIO 23
# Knap på GPIO 16 bruges til at starte sekvensen. Pull-up gør at den er '1' når ikke trykket.
left_fwd, left_bwd = Pin(18, Pin.OUT), Pin(22, Pin.OUT)
right_fwd, right_bwd = Pin(19, Pin.OUT), Pin(23, Pin.OUT)
button = Pin(16, Pin.IN, Pin.PULL_UP)

# --- Blink LED'er ---
# Brug en hardware-timer til at blinke alle LED'er hver 500 ms
Timer(0).init(
    period=500,  # tid i millisekunder
    mode=Timer.PERIODIC,
    callback=lambda t: [led.value(not led.value()) for led in leds]  # inverter LED-status
)

# --- Motorfunktioner ---

# Kør begge motorer fremad i et antal sekunder
def drive_forward(seconds):
    left_fwd.on(); left_bwd.off()       # Venstre motor frem
    right_fwd.on(); right_bwd.off()     # Højre motor frem
    time.sleep(seconds)                 # Vent i x sekunder
    stop()

# Kør begge motorer baglæns i et antal sekunder
def drive_backward(seconds):
    left_fwd.off(); left_bwd.on()       # Venstre motor baglæns
    right_fwd.off(); right_bwd.on()     # Højre motor baglæns
    time.sleep(seconds)
    stop()

# Drej venstre: højre motor fremad, venstre motor slukket
def turn_left(seconds):
    left_fwd.off(); left_bwd.off()      # Venstre motor stoppes
    right_fwd.on(); right_bwd.off()     # Højre motor frem
    time.sleep(seconds)
    stop()

# Drej højre: venstre motor fremad, højre motor slukket
def turn_right(seconds):
    left_fwd.on(); left_bwd.off()       # Venstre motor frem
    right_fwd.off(); right_bwd.off()    # Højre motor stoppes
    time.sleep(seconds)
    stop()

# Stop begge motorer
def stop():
    left_fwd.off(); left_bwd.off()
    right_fwd.off(); right_bwd.off()

# --- Hovedloop ---
# Vent på at knappen bliver trykket, og udfør en fast bevægelsessekvens
while True:
    if not button.value():  # Knappen er trykket ned (aktiv lav)
        drive_forward(3)    # Kør frem i 3 sekunder
        turn_left(1)        # Drej til venstre i 1 sekund
        drive_forward(3)    # Kør frem i 3 sekunder
        turn_right(1)       # Drej til højre i 1 sekund
        drive_backward(2)   # Bak i 2 sekunder

        # Vent til knappen bliver sluppet, så den ikke starter igen med det samme
        while not button.value():
            time.sleep(0.05)

