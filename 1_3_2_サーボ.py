from gpiozero import Servo
from time import sleep

myGPIO = 26                             # GPIOピン番号

myCorrection = 0.45                     # 補正係数
maxPW = (2.0 + myCorrection) / 1000     # 最大パルス幅
minPW = (1.0 - myCorrection) / 1000     # 最小パルス幅

servo = Servo(myGPIO, min_pulse_width=minPW, max_pulse_width=maxPW)

try:
    while True:
        servo.mid()     # 中央にする
        print("mid")
        sleep(0.5)

        servo.min()     # 最小にする
        print("min")
        sleep(1)

        servo.mid()     # 中央にする
        print("mid")
        sleep(0.5)

        servo.max()     # 最大にする
        print("max")
        sleep(1)

except KeyboardInterrupt:
    servo.mid()     # 中央にする
    sleep(1)
    print("終了します")
