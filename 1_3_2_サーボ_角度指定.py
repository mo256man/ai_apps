from gpiozero import AngularServo
from time import sleep

myGPIO = 26                             # GPIOピン番号

myCorrection = 0.45                     # 補正係数
maxPW = (2.0 + myCorrection) / 1000     # 最大パルス幅
minPW = (1.0 - myCorrection) / 1000     # 最小パルス幅

servo = AngularServo(myGPIO, min_pulse_width=minPW, max_pulse_width=maxPW)

try:
    while True:
        for a in range(-90, 90, 10):
            servo.angle = a
            sleep(0.1)

except KeyboardInterrupt:
    servo.mid()     # 中央にする
    sleep(1)
    print("終了します")
