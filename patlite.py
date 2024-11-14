import hid
import time

class Lr6usb():
    """
    LR6-USBクラス
    LEDを制御できます　ブザーは実装できていません　誰か改善してください
    """

    def __init__(self):
        """
        初期設定
        """
        vendor_id = 0x191A                  # ベンダーID
        product_id = 0x8003                 # プロダクトID
        self.is_available = True            # パトライトは有効（初期値）
        try:
            self.device = hid.device()      # HIDデバイス
            self.device.open(vendor_id, product_id)     # デバイスを開く
            self.clear()                    # パトライトのライトを全消し
        except Exception as e:              # デバイスを開けなかったら
            # print(e)                      # エラー内容
            self.is_available = False       # パトライト無効にする

    def clear(self):
        """
        ライト全消し
        """
        if self.is_available:               # パトライトが有効ならば
            command = [0] * 9               # コマンド　全部0
            self.device.write(command)      # デバイスにコマンドを書き込む

    def light(self, r=0, y=0, g=0, b=0, c=0):
        """
        ライト点灯　青と白は現物トライ未
        """
        if self.is_available:               # パトライトが有効ならば
            command = [0] * 9               # コマンド初期値　全部0
            command[5] = (r << 4) | y       # 赤と黄色
            command[6] = (g << 4) | b       # 緑と青
            command[7] = c << 4             # 白　下位4ビットは0
            self.device.write(command)      # デバイスにコマンドを書き込む
    
    def flash(self, r=0, y=0, g=0, b=0, c=0, fast=False):
        """
        ライト点滅　青と白は現物トライ未
        slow = Trueのとき、0.5秒間隔で点滅（デフォルト値）
        slow = Falseのとき、0.1秒間隔で点滅
        """
        if self.is_available:               # パトライトが有効ならば
            now = time.time()               # 現在時刻を秒で取得
            t = now - int(now)              # 整数部分を引き小数のみ残す
            t = int(t * 10)                 # 10倍して整数化 つまり0.1の位
            if fast:                        # fastならば
                cond = (t % 2 == 0)         # 条件は2で割り切れるか
            else:                           # fastでなければ
                cond = (t < 5)              # 条件は5未満かどうか

            if cond:                        # 条件を満たすならば
                self.light(r, y, g, b, c)   # 点灯
            else:                           # さもなくば
                self.clear()                # 消灯
    
def demo():
    """
    デモ
    """
    patlite = Lr6usb()                      # patliteをLR6-USBとして定義
    if patlite.is_available:                # パトライトが有効ならば
        pass                                # 特に何もしない
    else:                                   # 無効ならば
        print("LR6-USB not cnnected")       # メッセージ表示

    try:
        now = time.time()                   # 現在時刻（秒）
        while time.time() < now + 2:        # 2秒経過するまでループ
            pass                            # 何もしない

        now = time.time()                   # 現在時刻（秒）
        while time.time() < now + 3:        # 3秒経過するまでループ
            patlite.light(g=1)              # 緑を点灯

        now = time.time()                   # 現在時刻（秒）
        while time.time() < now + 3:        # 3秒経過するまでループ
            patlite.flash(y=1)              # 黄を点滅

        now = time.time()                   # 現在時刻（秒）
        while time.time() < now + 3:        # 3秒経過するまでループ
            patlite.flash(r=1, y=1, g=1, fast=True) # 赤黄緑を素早く点滅

        patlite.clear()                     # パトライト全消し
        print("終了しました")

    except KeyboardInterrupt:               # 途中でCtrl+Cで中断されたら
        patlite.clear()                     # パトライト全消し
        print("中断しました")

if __name__ == "__main__":                  # これが実行されたとき
    demo()                                  # デモを実行
