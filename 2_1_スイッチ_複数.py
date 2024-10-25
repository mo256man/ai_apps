#!/usr/bin/env python3
from gpiozero import Button
import cv2
from time import sleep

button1 = Button(13)				# 5番ピンをボタンとして使う
button2 = Button(19)				# 5番ピンをボタンとして使う

WIDTH, HEIGHT = 640, 480                    # カメラの幅と高さ
cap = cv2.VideoCapture(0)                   # ０番目のカメラにビデオキャプチャー定義
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)    # カメラ画像の横幅を設定
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)     # カメラ画像の縦幅を設定

is_puhed = False
btn_pushed = 0

while True:                                 # 無限ループ
    ret, frame = cap.read()                 # カメラの映像を取得する
    if ret:                                 # うまく取得できていたら
        print(is_puhed, btn_pushed)
        if not is_puhed:
            if button1.value:
                is_puhed = True
                btn_pushed =1
                print("button1 pushed")
                sleep(0.1)
            
            if button2.value:
                is_puhed = True
                btn_pushed =2
                print("button2 pushed")
                sleep(0.1)

            if not (button1.value or button2.value):
                print("waiting...")
        else:
            if button1.value:
                if btn_pushed != 1 :
                    print("1 is late")
                else:
                    print("btn1 reset")
                    btn_pushed = 0
                    is_puhed = False 

            if button2.value:
                if btn_pushed != 2 :
                    print("2 is late")
                else:
                    print("btn2 reset")
                    is_puhed = False 
                    btn_pushed = 0

        cv2.rectangle(frame, (0,0), (WIDTH, 25), (0, 0, 0), -1)
        
        x1 = int((btn_pushed-1)/ 2 * WIDTH)
        x2 = int(btn_pushed / 2 * WIDTH)
        
        cv2.rectangle(frame, (x1,0), (x2, 25), (100, 100, 255), -1)
        
        for i in [1, 2]:
            x = int((i - 0.5)/ 2 * WIDTH)
            cv2.putText(frame, f"{i}", (x,22),cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        



        cv2.imshow("camera", frame)         # 画像表示
        key = cv2.waitKey(1)                # キー入力を1マイクロ秒だけ待つ
        if key & 0xFF == 27:                # escキーが押されていたら
            break                           # 無限ループから抜ける
        elif key & 0xFF == 32:
            print("reset!")
            is_puhed = False            
            btn_pushed = 0

cap.release()                               # ビデオキャプチャーを解放する
cv2.destroyAllWindows()                     # OpenCVのウィンドウを全部閉じる
