from gpiozero import DistanceSensor
from time import sleep
import cv2

def draw_alarm(img, dis):
    # アラームを描画する関数
    msg = f"distance: {dis:.2f} cm"         # 元のメッセージ
    if dis < 5:                             # 5cmより近ければ
        msg += "  TOO CLOSE"                # メッセージに 近すぎ！ を追加
        color = (100, 100, 255)             # 背景色は赤
    elif dis > 20:                          # 20cmより遠ければ
        msg += "  TOO FAR"                  # メッセージに 遠すぎ！ を追加
        color = (255, 100, 100)             # 背景色は青
    else:                                   # どちらでもなければ
        color = (0, 0, 0)                   # 背景色は黒

    # 四角で塗りつぶす
    cv2.rectangle(frame, (0,0), (WIDTH, 25), color, -1)
    # メッセージ描画（日本語不可）     
    cv2.putText(frame, msg, (20,22), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    return frame                            # 加工した画像を返す

# ここからがメイン    
sensor = DistanceSensor(echo=24, trigger=23)    #距離センサーの設定
WIDTH, HEIGHT = 640, 480                    # カメラの幅と高さ
cap = cv2.VideoCapture(0)                   # ビデオキャプチャー定義
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)    # カメラ画像の横幅を設定
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)  # カメラ画像の縦幅を設定

fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")
output_name = "distance_sensor.mov"
video = cv2.VideoWriter(output_name, fourcc, 30, (WIDTH, HEIGHT)) 


while True:                                 # 無限ループ
    ret, frame = cap.read()                 # カメラの映像を取得する
    if ret:                                 # うまく取得できていたら
        dis = sensor.distance * 100			# 距離（センチメートル）
        frame = draw_alarm(frame, dis)      # アラーム描画
        cv2.imshow("camera", frame)         # 画像表示
        video.write(frame)
        key = cv2.waitKey(1)                # キー入力を1マイクロ秒だけ待つ
        if key & 0xFF == 27:                # escキーが押されていたら
            break                           # 無限ループから抜ける

cap.release()                               # ビデオキャプチャーを解放する
cv2.destroyAllWindows()                     # OpenCVのウィンドウを全部閉じる
video.release()
