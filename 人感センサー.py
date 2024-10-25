from gpiozero import MotionSensor
import cv2
import time

pir = MotionSensor(26)
pir.wait_for_motion()

WIDTH, HEIGHT = 640, 480                    # カメラの幅と高さ
cap = cv2.VideoCapture(0)                   # ０番目のカメラにビデオキャプチャー定義
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)    # カメラ画像の横幅を設定
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)     # カメラ画像の縦幅を設定

while True:                                 # 無限ループ
    ret, frame = cap.read()                 # カメラの映像を取得する
    if ret:                                 # うまく取得できていたら
        if pir.value:
            msg = "Motion Detected"
            print(msg)
            color = (100, 100, 255)         # 色 赤
        else:
            msg=""
            color = (0, 0, 0)               # 色 黒

        # 指定した色で四角形を塗りつぶす
        cv2.rectangle(frame, (0,0), (WIDTH, 25), color, -1)

        # テキスト描画（日本語不可）
        cv2.putText(frame, msg, (20,22),cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

        cv2.imshow("camera", frame)         # 画像表示
        key = cv2.waitKey(1)                # キー入力を1マイクロ秒だけ待つ
        if key & 0xFF == 27:                # escキーが押されていたら
            break                           # 無限ループから抜ける

cap.release()                               # ビデオキャプチャーを解放する
cv2.destroyAllWindows()                     # OpenCVのウィンドウを全部閉じる
