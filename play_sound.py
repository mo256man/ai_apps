import pygame
import datetime

filename = "alarm.mp3"                  # ファイル名
pygame.mixer.init()                     # mixerモジュール初期化
pygame.mixer.music.load(filename)       # 音源取り込み

while True:                             # 無限ループ（Ctrl+Cで中断）
    dt = datetime.datetime.now()        # 現在日時
    second = dt.second                  # 現在日時の秒

    if second < 5:                      # 秒が5未満ならば
        is_playable = True              # 再生させる設定オン
    else:                               # さもなくば
        is_playable = False             # 再生させる設定オフ
    
    is_busy = pygame.mixer.music.get_busy()     # 再生中かどうか
    if is_playable:                     # 再生させる設定ならば
        if is_busy:                     # 再生中ならば
            pass                        # 何もしない
        else:                           # さもなくば
            pygame.mixer.music.play()   # 音楽再生させる
    else:                               # 再生させる設定でなければ
        pygame.mixer.music.stop()       # 音楽停止する
