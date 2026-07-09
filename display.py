# 縦16*横24くらいで、「温度：」「湿度：」（TEMP, HUMIでも可）をビットマップで作り、
# SSD1306でグラフィック表示できるようにすること

from machine import Pin, I2C
from myDisplay import Display
import time

i2c = I2C(0, sda=Pin(16), scl=Pin(17))
display = Display(i2c)

button = Pin(12, Pin.IN, Pin.PULL_UP)

mode = 0
last_button = 1

i = 0
while True:
    current_button = button.value()

    if last_button == 1 and current_button == 0:
        mode ^= 1

    last_button = current_button
    
    i += 1
    display.fill(0)
    display.text2x(f"T:{i:4.1f}C", 0, 0)
    display.text2x(f"MODE:{mode}", 0, 16)
    display.show()
    time.sleep(1)
