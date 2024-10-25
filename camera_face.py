#!/usr/bin/env python3

import cv2

WIDTH, HEIGHT = 640, 480                    # カメラの幅と高さ
cap = cv2.VideoCapture(0)                   # ０番目のカメラにビデオキャプチャー定義
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)    # カメラ画像の横幅を設定
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)     # カメラ画像の縦幅を設定

cascade_path = "./models/haarcascade_frontalface_alt2.xml"
cascade = cv2.CascadeClassifier(cascade_path)

while True:                                 # 無限ループ
    ret, frame = cap.read()                 # カメラの映像を取得する
    if ret:                                 # うまく取得できていたら
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
        
        faces = cascade.detectMultiScale(gray)
        if len(faces) > 0:
            for face in faces:
                x, y, w, h = face

                # 検出した顔の範囲をモザイクする
                roi = frame[y:y+h, x:x+w]
                roi = cv2.resize(roi, (w//10, h//10))
                roi = cv2.resize(roi, (w, h), interpolation=cv2.INTER_NEAREST)
                frame[y:y+h, x:x+w] = roi 

                # 検出した顔の範囲を四角で囲む
                frame = cv2.rectangle(frame, (x, y), (x+w, y+h), color=(255, 255, 255), thickness=2)
        
        cv2.imshow("camera", frame)         # 画像表示
        key = cv2.waitKey(1)                # キー入力を1マイクロ秒だけ待つ
        if key & 0xFF == 27:                # escキーが押されていたら
            break                           # 無限ループから抜ける

cap.release()                               # ビデオキャプチャーを解放する
cv2.destroyAllWindows()                     # OpenCVのウィンドウを全部閉じる
