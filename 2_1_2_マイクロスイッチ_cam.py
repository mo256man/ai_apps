
from gpiozero import Button
from time import sleep
import cv2

# 17番ピンをマイクロスイッチとして使う
micro_switch = Button(17)

WIDTH, HEIGHT = 640, 480                    # カメラの幅と高さ
cap = cv2.VideoCapture(0)                   # 0番目のカメラにビデオキャプチャー定義
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)    # カメラ画像の横幅を設定
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)  # カメラ画像の縦幅を設定

while True:
    ret, frame = cap.read()
    if ret:
        if micro_switch.is_pressed:         # マイクロスイッチが押されたら
            msg = "SWITCH ON"
            color = (100, 100, 255)         # 色 赤
        else:                               # さもなくば
            msg = ""
            color = (255, 100, 100)         # 色 青

        # 指定した色で四角形を塗りつぶす
        cv2.rectangle(frame, (0,0), (WIDTH, 25), color, -1)

        # テキスト描画（日本語不可）
        cv2.putText(frame, msg, (20,22),cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

        cv2.imshow("camera", frame)
        key = cv2.waitKey(1)
        if key & 0xFF == 27:
            break
        elif key & 0xFF == ord("z"):
            cv2.imwrite("micro1.jpg", frame)
        elif key & 0xFF == ord("x"):
            cv2.imwrite("micro2.jpg", frame)

cv2.destroyAllWindows()
