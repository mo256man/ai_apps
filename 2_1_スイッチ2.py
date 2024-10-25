#!/usr/bin/env python3
from gpiozero import LED, Button 
from signal import pause

# button = Button(26, pull_up=True)				# 5番ピンをボタンとして使う
button = Button(13)				# 5番ピンをボタンとして使う
led = LED(17)					# 17番ピンをLEDとして使う

while True:
    if button.value:
        led.on()
        print("LED ON")
    else:
        led.off()
        print("LED OFF")

