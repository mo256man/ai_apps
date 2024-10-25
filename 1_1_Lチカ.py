#!/usr/bin/env python3
from gpiozero import LED
from time import sleep

led = LED(17)				# 17番ピンをLEDとして使う

try:
	while True:				# 無限ループ
		led.on()				# LED点灯
		print("点灯")			# メッセージ
		sleep(0.5)				# 0.5秒止まる

		led.off()				# LED消灯
		print("消灯")			# メッセージ
		sleep(0.5)				# 0.5秒止まる

except KeyboardInterrupt:	# ctrl+Cで中断したら
	LED.off()				# LED消灯
	print("終了します")		# メッセージ
