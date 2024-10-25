from gpiozero import LED, Button
from time import sleep

# 17番ピンをマイクロスイッチとして使う
# pull_up=False を pull_up=True に変更してトライしてみてください
micro_switch = Button(17, pull_up=False)
led1 = LED(22)                          # 22番ピンをLED1として使う
led2 = LED(27)                          # 27番ピンをLED2として使う

while True:
    if micro_switch.is_pressed:         # マイクロスイッチが押されたら
        print('LED1 ON')                # "LED1 ON"と表示
        led1.on()                       # LED1を点灯する
        led2.off()                      # LED2を消灯する
    else:                               # さもなくば
        print('    LED2 ON')            # LED1とはずれた位置で"LED2 ON"と表示
        led1.off()                      # LED1を消灯する
        led2.on()                       # LED2を点灯する

    sleep(0.5)                          # 0.5秒休む
