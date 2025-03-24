from machine import Pin
from time import sleep

# Output pins
output_pins = [4, 16, 17, 5]
outputs = [Pin(pin, Pin.OUT) for pin in output_pins]

# Button on D2
button = Pin(15, Pin.IN, Pin.PULL_UP)  # Active LOW

current_index = -1  # Start with all outputs off

# Turn off all outputs initially
for out in outputs:
    out.value(0)

while True:
    # Wait for button press
    if button.value() == 0:
        # Turn off current output
        if current_index != -1:
            outputs[current_index].value(0)

        # Move to next output
        current_index = (current_index + 1) % len(outputs)

        # Turn on new output
        outputs[current_index].value(1)
        print(f"Output {output_pins[current_index]} is ON")

        # Wait for button to be released before continuing
        while button.value() == 0:
            sleep(0.01)

    sleep(0.01)  # Loop delay

