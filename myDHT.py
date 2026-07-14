# =============================================================================
# Pico DHT11センサー制御（PIOステートマシン）
# =============================================================================

import time
from machine import Pin
from rp2 import PIO, StateMachine, asm_pio

# ---- PIO0: DHT11制御（ステートマシン） ----
@asm_pio(sideset_init=PIO.OUT_HIGH, autopush=True, push_thresh=8)
def dht11_protocol():
    """
    DHT11通信プロトコルのPIOプログラム。
    1. STARTシグナルを送る（20ms LOW）
    2. DHT11のレスポンスを受け取る（80μs LOW, 80μs HIGH）
    3. 40ビットのデータを読み込む（各ビット：LOW後、26-28μs HIGH=0 or 70μs HIGH=1）
    """
    # START信号（20ms LOW）：出力方向にしてピンをLOWに駆動
    set(pindirs, 1)
    set(pins, 0)
    set(x, 31)
    label("start_low")
    nop()
    jmp(x_dec, "start_low")
    
    # 入力方向に戻してDHT11からの応答を待つ
    set(pindirs, 0)
    set(x, 31)
    label("wait_resp_low")
    jmp(pin, "wait_resp_low")
    
    # DHT11レスポンス（80μs LOW）
    set(x, 15)
    label("resp_low")
    nop()
    jmp(x_dec, "resp_low")
    
    # 40ビット読み込み
    set(y, 39)
    label("read_bits")
    
    # 各ビット：LOW期間（50μs）
    set(x, 9)
    label("bit_low")
    jmp(x_dec, "bit_low")
    
    # HIGH期間を計測（26-28μs=0, 70μs=1）
    set(x, 15)
    label("bit_high")
    jmp(pin, "bit_high_end")
    jmp(x_dec, "bit_high")
    
    label("bit_high_end")
    in_(pins, 1)
    jmp(y_dec, "read_bits")


class DHT11PIO:
    """PIOを使ったDHT11センサー制御"""
    def __init__(self, pin_num):
        self.pin = Pin(pin_num, Pin.IN, Pin.PULL_UP)
        self.sm = StateMachine(0, dht11_protocol, freq=2000000,
                               set_base=self.pin, jmp_pin=self.pin, in_base=self.pin)
        self.sm.active(1)
    
    def measure(self):
        """DHT11を測定（temp, humi）を返す。失敗時はNone"""
        try:
            self.sm.put(0)
            time.sleep_ms(100)
            
            if self.sm.rx_fifo() >= 5:
                data = 0
                for i in range(5):
                    data = (data << 8) | self.sm.get()
                
                humi_int = (data >> 32) & 0xFF
                humi_frac = (data >> 24) & 0xFF
                temp_int = (data >> 16) & 0xFF
                temp_frac = (data >> 8) & 0xFF
                checksum = data & 0xFF
                
                if ((humi_int + humi_frac + temp_int + temp_frac) & 0xFF) == checksum:
                    temp = temp_int + temp_frac / 256.0
                    humi = humi_int
                    return round(temp, 1), int(humi)
        except Exception:
            pass
        
        return None
