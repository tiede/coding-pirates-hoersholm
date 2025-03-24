from machine import Pin
from time import sleep_ms, ticks_ms, ticks_diff
import urandom

# --- Hardware opsætning ---
led = Pin(2, Pin.OUT)  # LED på D2
buttons = [
    Pin(15, Pin.IN, Pin.PULL_UP),  # D15 - Spiller 1
    Pin(4, Pin.IN, Pin.PULL_UP),   # D4  - Spiller 2
    Pin(16, Pin.IN, Pin.PULL_UP),  # D16 - Spiller 3
    Pin(17, Pin.IN, Pin.PULL_UP)   # D17 - Spiller 4
]

# --- Spilopsætning ---
num_players = int(input("Indtast antal spillere (1–4): "))
assert 1 <= num_players <= 4, "Antal spillere skal være mellem 1 og 4"

WIN_SCORE = int(input("Indtast antal point for at vinde (f.eks. 10): "))
assert WIN_SCORE > 0, "Point skal være større end 0"

# Indlæs spillernavne
player_names = []
for i in range(num_players):
    name = input(f"Indtast navn for spiller {i + 1}: ")
    player_names.append(name)

# Initialiser score og statistik
scores = [0] * num_players
reaction_sums = [0] * num_players
reaction_counts = [0] * num_players

ROUND_DELAY = [2000, 5000]  # ms


# --- Funktioner ---

def countdown():
    """Vis nedtælling én gang før spillet starter."""
    print("Gør dig klar...")
    for i in range(3, 0, -1):
        print(i)
        sleep_ms(1000)

def wait_for_release(player_index):
    """Vent til spilleren slipper knappen (anti-bounce)."""
    while buttons[player_index].value() == 0:
        sleep_ms(10)

def wait_for_random_start():
    """
    Vent en tilfældig tid. Hvis nogen trykker for tidligt, returnér fejl.
    Ellers returnér 'go' når LED tændes.
    """
    led.value(0)
    wait_time = urandom.getrandbits(10) % (ROUND_DELAY[1] - ROUND_DELAY[0]) + ROUND_DELAY[0]
    for _ in range(wait_time // 10):
        for i in range(num_players):
            if buttons[i].value() == 0:
                wait_for_release(i)
                return f"p{i}_false"
        sleep_ms(10)
    led.value(1)
    return "go"

def wait_for_winner():
    """Vent på at en spiller trykker efter LED er tændt og returnér deres reaktionstid."""
    start = ticks_ms()
    while True:
        for i in range(num_players):
            if buttons[i].value() == 0:
                reaction_time = ticks_diff(ticks_ms(), start)
                wait_for_release(i)
                return i, reaction_time
        sleep_ms(1)

def print_scores():
    """Vis kun point efter hver runde."""
    print("\nStilling:")
    for i in range(num_players):
        print(f"{player_names[i]}: {scores[i]} point")

def print_final_stats():
    """Vis slutstatistik med gennemsnitlig reaktionstid."""
    print("\nSlutstatistik:")
    for i in range(num_players):
        avg = reaction_sums[i] // reaction_counts[i] if reaction_counts[i] > 0 else "-"
        print(f"{player_names[i]}: {scores[i]} point | Gennemsnitlig reaktionstid: {avg} ms")


# --- Spilstart ---
print("\n🎮 Refleks-spil starter!")
countdown()  # Kun første gang

# --- Spil-loop ---
while max(scores) < WIN_SCORE:
    print("\n--- Ny runde ---")
    result = wait_for_random_start()

    if result != "go":
        # For tidligt tryk
        i = int(result[1])
        scores[i] = max(0, scores[i] - 1)
        print(f"{player_names[i]} trykkede for tidligt! -1 point.")
        print_scores()
        continue

    # Gyldigt tryk – registrer vinder og tid
    winner, reaction_time = wait_for_winner()
    scores[winner] += 1
    reaction_sums[winner] += reaction_time
    reaction_counts[winner] += 1
    print(f"{player_names[winner]} vinder runden! Reaktionstid: {reaction_time} ms")
    print_scores()
    led.value(0)
    sleep_ms(1000)

# --- Spillet er slut ---
led.value(1)
winner = scores.index(max(scores))
print(f"\n🎉 {player_names[winner]} VINDER SPILLET! 🎉")
print_final_stats()
