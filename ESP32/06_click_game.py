from machine import Pin
from time import sleep_ms, ticks_ms, ticks_diff
import urandom  # Bruges til at generere tilfældig ventetid

# --- Hardware opsætning ---

# LED på D2, bruges til at signalere "GO"
led = Pin(2, Pin.OUT)

# Liste af knapper til spillere:
# PULL_UP betyder, at knappen er aktiv lav (0 når trykket)
buttons = [
    Pin(15, Pin.IN, Pin.PULL_UP),  # Spiller 1 - D15
    Pin(4, Pin.IN, Pin.PULL_UP),   # Spiller 2 - D4
    Pin(16, Pin.IN, Pin.PULL_UP),  # Spiller 3 - D16
    Pin(17, Pin.IN, Pin.PULL_UP)   # Spiller 4 - D17
]

# --- Spilopsætning ---

# Spørg brugeren hvor mange spillere der deltager
num_players = int(input("Indtast antal spillere (1–4): "))
assert 1 <= num_players <= 4, "Antal spillere skal være mellem 1 og 4"

# Spørg hvor mange point der skal til for at vinde
WIN_SCORE = int(input("Indtast antal point for at vinde (f.eks. 10): "))
assert WIN_SCORE > 0, "Point skal være større end 0"

# Score og reaktionstids-tracking for hver spiller
scores = [0] * num_players               # Point for hver spiller
reaction_sums = [0] * num_players        # Summeret reaktionstid
reaction_counts = [0] * num_players      # Antal gyldige reaktioner

# Tiden der ventes tilfældigt mellem 2 og 5 sekunder før LED tændes
ROUND_DELAY = [2000, 5000]  # i millisekunder


# --- Funktioner ---

def countdown():
    """Vis en nedtælling i konsollen før spillet starter."""
    print("Gør dig klar...")
    for i in range(3, 0, -1):
        print(i)
        sleep_ms(1000)

def wait_for_release(player_index):
    """Vent på at spilleren slipper knappen (anti-bounce og undgår gentagne tryk)."""
    while buttons[player_index].value() == 0:
        sleep_ms(10)

def wait_for_random_start():
    """
    Vent en tilfældig tid og overvåg om nogen trykker for tidligt.
    Returnerer 'go' hvis alle venter korrekt, ellers 'pX_false' hvis spiller X snyder.
    """
    led.value(0)  # Sluk LED som startsignal
    wait_time = urandom.getrandbits(10) % (ROUND_DELAY[1] - ROUND_DELAY[0]) + ROUND_DELAY[0]
    for _ in range(wait_time // 10):
        for i in range(num_players):
            if buttons[i].value() == 0:  # Spilleren trykkede for tidligt
                wait_for_release(i)
                return f"p{i}_false"
        sleep_ms(10)
    led.value(1)  # Tænd LED som "GO!"
    return "go"

def wait_for_winner():
    """
    Vent på at en spiller trykker efter LED er tændt.
    Returnerer spillernummer og reaktionstid i millisekunder.
    """
    start = ticks_ms()  # Gem tidspunkt for LED tænding
    while True:
        for i in range(num_players):
            if buttons[i].value() == 0:
                reaction_time = ticks_diff(ticks_ms(), start)
                wait_for_release(i)
                return i, reaction_time
        sleep_ms(1)

def print_scores():
    """Vis den aktuelle score (uden gennemsnit)."""
    print("\nStilling:")
    for i in range(num_players):
        print(f"Spiller {i + 1}: {scores[i]} point")

def print_final_stats():
    """Vis slutstatistik med gennemsnitlig reaktionstid for hver spiller."""
    print("\nSlutstatistik:")
    for i in range(num_players):
        avg = reaction_sums[i] // reaction_counts[i] if reaction_counts[i] > 0 else "-"
        print(f"Spiller {i + 1}: {scores[i]} point | Gennemsnitlig reaktionstid: {avg} ms")


# --- Spil-start ---
print("\n🎮 Refleks-spil starter!")
countdown()  # Kun én gang før første runde

# --- Spil-loop ---
while max(scores) < WIN_SCORE:
    print("\n--- Ny runde ---")
    result = wait_for_random_start()

    if result != "go":
        # En spiller trykkede for tidligt
        i = int(result[1])  # Udtræk spillernummer fra fx "p0_false"
        scores[i] = max(0, scores[i] - 1)  # Træk 1 point fra, men ikke under 0
        print(f"Spiller {i + 1} trykkede for tidligt! -1 point.")
        print_scores()
        continue

    # En spiller har vundet runden korrekt
    winner, reaction_time = wait_for_winner()
    scores[winner] += 1
    reaction_sums[winner] += reaction_time
    reaction_counts[winner] += 1
    print(f"Spiller {winner + 1} vinder runden! Reaktionstid: {reaction_time} ms")
    print_scores()
    led.value(0)  # Sluk LED igen
    sleep_ms(1000)

# --- Spillet er slut ---
led.value(1)  # Tænd LED for at vise spillet er slut
winner = scores.index(max(scores))
print(f"\n🎉 Spiller {winner + 1} VINDER SPILLET! 🎉")
print_final_stats()
