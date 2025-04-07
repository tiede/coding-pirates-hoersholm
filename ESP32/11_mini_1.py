import machine
import time

# Morse-kode ordbog: Oversætter bogstaver og tal til morsekode
MORSE_CODE_DICT = {
    'A': '.-',     'B': '-...',   'C': '-.-.', 
    'D': '-..',    'E': '.',      'F': '..-.',
    'G': '--.',    'H': '....',   'I': '..',
    'J': '.---',   'K': '-.-',    'L': '.-..',
    'M': '--',     'N': '-.',     'O': '---',
    'P': '.--.',   'Q': '--.-',   'R': '.-.',
    'S': '...',    'T': '-',      'U': '..-',
    'V': '...-',   'W': '.--',    'X': '-..-',
    'Y': '-.--',   'Z': '--..',
    '1': '.----',  '2': '..---',  '3': '...--',
    '4': '....-',  '5': '.....',  '6': '-....',
    '7': '--...',  '8': '---..',  '9': '----.',
    '0': '-----',  ' ': '/'  # Bruges til mellemrum i sætninger
}

# Initialiser GPIO2 som udgang til LED
led = machine.Pin(2, machine.Pin.OUT)

# Tidsindstillinger for morsekode
DOT = 0.2              # En prik varer 0.2 sekunder
DASH = DOT * 3         # En streg varer tre gange så længe som en prik
SYMBOL_SPACE = DOT     # Pause mellem prikker og streger i ét bogstav
LETTER_SPACE = DOT * 3 # Pause mellem bogstaver
WORD_SPACE = DOT * 7   # Pause mellem ord

# Funktion til at blinke morsekode for en given tekst
def blink_morse(message):
    print("\nMorseoutput:")
    for char in message.upper():
        code = MORSE_CODE_DICT.get(char, '')
        if not code:
            continue  # Spring tegn over som ikke findes i ordbogen

        if code == '/':
            # Mellemrum mellem ord
            print(' ', end='  ')
            time.sleep(WORD_SPACE)
        else:
            # Print tegn og tilsvarende morsekode
            print(f"{char}: {code}")
            for symbol in code:
                if symbol == '.':
                    led.on()
                    time.sleep(DOT)
                elif symbol == '-':
                    led.on()
                    time.sleep(DASH)
                led.off()
                time.sleep(SYMBOL_SPACE)
            time.sleep(LETTER_SPACE)
    print("Færdig.\n")

# Hovedloop: Spørger brugeren om input og blinker det i morsekode
while True:
    msg = input("Skriv en besked (Ctrl+C for at stoppe): ")
    blink_morse(msg)
