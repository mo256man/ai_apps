from gpiozero import LED
import datetime

led_pin = 17
led = LED(led_pin)

def led_flash():
    """
    0.5秒間隔で点滅する関数
    """
    dt = datetime.datetime.now()    # 現在日時
    microsec = dt.microsecond       # 現在日時のマイクロ秒（整数の秒は含まない）
    fractional_second = microsec / 1_000_000  # 100万で割って秒にする
    if fractional_second < 0.5:     # 秒以下の値が0.5未満ならば
        led.on()                    # LED点灯する
    else:                           # さもなくば
        led.off()                   # 消灯する

# ここからがメイン        
while True:                         # 無限ループ（Ctrl+Cで中断）
    dt = datetime.datetime.now()    # 現在日時
    second = dt.second              # 現在日時の秒
    second_unit = second % 10       # 秒を10で割ったときの余り
    if second_unit < 4:             # 余りが4未満ならば
        led.off()                   # LED消灯
    elif 4 <= second_unit < 7:      # 4以上7未満ならば
        led_flash()                 # LED点滅
    else:                           # さもなくば つまり7以上ならば
        led.on()                    # LED点灯

