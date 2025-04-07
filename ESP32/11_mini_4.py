from machine import Pin
from time import sleep
import urandom

led = Pin(2, Pin.OUT)

# Morse timing (kan justeres)
DOT = 0.2
DASH = DOT * 3
GAP = DOT

morse_chars = ['.', '-']

# Blink LED som dot eller dash
def blink(symbol):
    led.on()
    sleep(DOT if symbol == '.' else DASH)
    led.off()
    sleep(GAP)

# Lav tilfældigt morsemønster
def generate_morse(length):
    return ''.join(urandom.choice(morse_chars) for _ in range(length))

# Afspil morsekode med LED
def play_morse(code):
    for symbol in code:
        blink(symbol)
        sleep(GAP)

# Start spillet
def start_game():
    print("Starter morse-spil!")
    score = 0
    level = 1

    while True:
        print(f"\nLevel {level} – mønster vises:")
        code = generate_morse(level + 1)
        sleep(1)
        play_morse(code)
        sleep(0.5)

        guess = input("Indtast mønster (brug . for kort og - for lang): ").strip()
        if guess == code:
            score += 1
            level += 1
            print("✔️ Korrekt! Point:", score)
        else:
            print("❌ Forkert! Det rigtige var:", code)
            print("Slutscore:", score)
            break

# Venter på 'start' kommando
while True:
    cmd = input("Skriv 'start' for at begynde: ").strip().lower()
    if cmd == 'start':
        start_game()

