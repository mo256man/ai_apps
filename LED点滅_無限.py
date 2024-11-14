from gpiozero import LED
import time

led_pin = 17
led = LED(led_pin)

while True:
    led.on()
    time.sleep(0.5)
    led.off()
    time.sleep(0.5)

