#!/usr/bin/env python3
from gpiozero import DistanceSensor
from time import sleep

# 24番ピンをエコー、23番ピンをトリガーの距離センサーとして使う
sensor = DistanceSensor(echo=24, trigger=23)

while True:                             # 無限ループ
    dis = sensor.distance * 100	        # センチメートルにする
    print(f"distance: {dis:.2f} cm")    # 結果表示
    sleep(0.3)                          # 0.3秒休む
