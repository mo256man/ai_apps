from gpiozero import DistanceSensor
from time import sleep
from patlite import Lr6usb

# 距離センサーの設定
sensor = DistanceSensor(echo=19, trigger=26)

patlite = Lr6usb()

try:
    while True:                             # 無限ループ
        dis = sensor.distance * 100			# 距離（センチメートル）
        msg = f"distance: {dis:.2f} cm"     # メッセージ
        print(msg)
        if dis < 5:                         # 5cmより近ければ
            patlite.flash(red=1)
        elif dis > 20:                      # 20cmより遠ければ
            patlite.light(green=1)
        else:                               # どちらでもなければ
            patlite.flash(yellow=1)

except KeyboardInterrupt:                   # ctrl+cでプロフラム中止したら
    patlite.clear()                         # パトライト消灯する
