import machine
import time

# GPIO-opsætning
led = machine.Pin(2, machine.Pin.OUT)             # LED på GPIO2
button = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)  # Knap på GPIO16 med intern pull-up

# Tæller til antal tryk
count = 0

# Funktion til at blinke LED én gang
def blink(times=1, duration=0.2):
    for _ in range(times):
        led.on()
        time.sleep(duration)
        led.off()
        time.sleep(0.1)

# Hovedloop
print("Tryk på knappen for at tælle op. Hold inde i 3 sekunder for at nulstille.")
last_state = 1
press_start = 0

while True:
    current_state = button.value()

    if last_state == 1 and current_state == 0:
        # Knap er lige blevet trykket ned
        press_start = time.ticks_ms()

    elif last_state == 0 and current_state == 1:
        # Knap er lige blevet sluppet
        press_duration = time.ticks_diff(time.ticks_ms(), press_start)

        if press_duration >= 3000:
            count = 0
            print("Tæller nulstillet.")
            blink(3, 0.1)
        else:
            count += 1
            print("Antal tryk:", count)
            blink()

    last_state = current_state
    time.sleep(0.01)  # Lidt delay til debounce

