import network, espnow, sys

# 1. Aktivér WiFi-station
w = network.WLAN(network.STA_IF)
w.active(True)
# (valgfrit) sæt kanal – alle modtagere SKAL bruge samme kanal
# w.config(channel=6)

# 2. Initialisér ESP-NOW
e = espnow.ESPNow()
e.active(True)

# 3. Tilføj broadcast-peer
broadcast = b'\xFF\xFF\xFF\xFF\xFF\xFF'
e.add_peer(broadcast)

print("ESP-NOW broadcast klar. Skriv din besked og tryk Enter. Ctrl-C for at afslutte.")

# 4. Loop: læs besked fra brugeren og send
while True:
    try:
        # input() virker i MicroPython REPL
        msg = input("Besked ▶ ")
    except KeyboardInterrupt:
        print("\nAfslutter sender.")
        break
    if not msg:
        # spring over tomme beskeder
        continue

    # konverter til bytes og send
    ok = e.send(broadcast, msg.encode('utf-8'))
    print("Sendt:" , ok)
