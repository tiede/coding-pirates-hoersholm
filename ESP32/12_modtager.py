import network, espnow, time

# 1. WiFi-station on
w = network.WLAN(network.STA_IF)
w.active(True)

# samme kanal hvis sat
# w.config(channel=6)

# 2. ESPNow klar
e = espnow.ESPNow()
e.active(True)

# 3. Tilføj Kort A som peer
#peer = bytes([0xDE,0xAD,0xBE,0xEF,0x00,0x01])
#e.add_peer(peer)

# 4. Modtag i loop
print('Venter på beskeder…')
while True:
    host, msg = e.recv()      # blokkerer indtil data
    if host:
        src = ':'.join(f'{b:02X}' for b in host)
        print(f'Fra {src}: {msg}')
    time.sleep_ms(100)

