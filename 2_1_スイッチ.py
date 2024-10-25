#!/usr/bin/env python3
from gpiozero import LED, Button 
from signal import pause

led = LED(17)					# 17番ピンをLEDとして使う
button = Button(5)				# 5番ピンをボタンとして使う

button.when_pressed = led.on	# ボタンが押されたらLED点灯
button.when_released = led.off	# ボタンが離されたらLED消灯

pause()							# イベント発生するまで何もせず待つ
