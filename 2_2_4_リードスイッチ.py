from gpiozero import LED, Button

reed_switch = Button(17, pull_up=True)  # Reed switch on GPIO 17, using an internal pull-up resistor
green_led = LED(27)                     # Green LED connected to GPIO pin 27
red_led = LED(22)                       # Red LED connected to GPIO pin 22

def update_leds():
    if reed_switch.is_pressed:
        green_led.off()          # Turn off the green LED
        red_led.on()             # Turn on the red LED
    else:
        green_led.on()           # Turn on the green LED
        red_led.off()            # Turn off the red LED

try:
    green_led.on()               # Turn on the green LED at the start
    while True:
        # Set the callback functions for reed switch state changes
        reed_switch.when_pressed = update_leds   # Callback when the switch is pressed
        reed_switch.when_released = update_leds  # Callback when the switch is released


except KeyboardInterrupt:
    green_led.off()
    red_led.off()
    pass
