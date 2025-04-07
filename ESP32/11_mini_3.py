import machine
import time

# GPIO-opsætning
led_pwm = machine.PWM(machine.Pin(2), freq=1000)  # LED på GPIO2 med PWM
button = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)

# Lysstyrkeniveauer i procent (0–1023 for ESP32 PWM duty)
levels = [0, 256, 512, 768, 1023]
level_index = 0

# Funktion til at opdatere lysstyrke
def update_led():
    duty = levels[level_index]
    led_pwm.duty(duty)
    print(f"Lysstyrke: {int(duty / 1023 * 100)}%")

# Hjælp til debounce
def wait_for_release():
    while button.value() == 0:
        time.sleep(0.01)

print("Tryk på knappen for at skifte lysstyrke (0–100%)\n")

# Start med første niveau
update_led()

# Hovedloop
while True:
    if button.value() == 0:
        wait_for_release()
        level_index = (level_index + 1) % len(levels)
        update_led()
        time.sleep(0.2)  # Lidt delay for debounce

