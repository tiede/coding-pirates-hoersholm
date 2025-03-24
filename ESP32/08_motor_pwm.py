from machine import Pin, PWM
from time import sleep

# Output pins
output_pins = [4, 16, 17, 5]

# Set up PWM on each pin
outputs = [PWM(Pin(pin), freq=1000, duty=0) for pin in output_pins]

# Button on D2
button = Pin(2, Pin.IN, Pin.PULL_UP)  # Active LOW

current_index = -1  # Start with all outputs off
duty_cycle = 512    # PWM duty (range: 0–1023)

# Ensure all outputs are off initially
for pwm in outputs:
    pwm.duty(0)

while True:
    if button.value() == 0:
        # Turn off current PWM output
        if current_index != -1:
            outputs[current_index].duty(0)

        # Move to next output
        current_index = (current_index + 1) % len(outputs)

        # Turn on new PWM output
        outputs[current_index].duty(duty_cycle)
        print(f"PWM on GPIO {output_pins[current_index]} at 50% duty")

        # Wait for button release
        while button.value() == 0:
            sleep(0.01)

    sleep(0.01)
