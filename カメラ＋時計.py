# カメラ起動を早くするおまじない
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

import datetime
import cv2
WIDTH, HEIGHT = 1280, 720                   # 幅と高さ
cap = cv2.VideoCapture(0)                   # ビデオキャプチャー設定
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)    # 幅設定
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)  # 高さ設定
WHITE = (255, 255, 255)                     # 白色

while True:                                 # 無限ループ
    ret, frame = cap.read()                 # 画像取得
    if ret:                                 # 画像が正しく取得できていたら
        dt = datetime.datetime.now()        # 現在日時を取得（datetime型）
        str_dt = dt.strftime("%m/%d %H:%M:%S")      # 文字列にする
        cv2.putText(frame, str_dt, (25,25), cv2.FONT_HERSHEY_SIMPLEX, 1, WHITE, 2)  # 日時を描画
        cv2.imshow("camera", frame)         # 画像表示

        key = cv2.waitKey(1)                # キー入力を1マイクロ秒だけ待つ
        if key & 0xFF == 27:                # escキーが押されていたら
            break                           # 無限ループから抜ける

cv2.destroyAllWindows()                     # 画像ウィンドウを閉じる
cap.release()                               # ビデオキャプチャーを解放する
