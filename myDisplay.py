# =============================================================================
# Pico ディスプレイ制御（SPI）とボタン管理
# =============================================================================

import time
from machine import Pin, SPI
import framebuf
from myColor import Color

# ---- SPI制御（ステートマシン - 参考用） ----
# PIOのSPI実装は複雑なため、実装ではmachine.SPIを使用
# @asm_pio(sideset_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_LEFT)
# def spi_protocol():
#     """
#     SPI通信をPIOで実装。
#     CLK（sideset）、MOSI（データ出力）を制御。
#     8ビットのデータをMSBファーストで送信。
#     """
#     label("start")
#     pull(block)
#     set(x, 7)
#     label("send_bit")
#     out(pins, 1)  .side(0)
#     nop()         .side(1)
#     jmp(x_dec, "send_bit")
#     jmp("start")


class DisplayPIO:
    """SPI経由のディスプレイ制御（machine.SPI使用）"""
    def __init__(self, cs_pin, reset_pin, a0_pin, clk_pin, mosi_pin, led_pin=None, width=128, height=160):
        self.cs = Pin(cs_pin, Pin.OUT, value=1)
        self.reset = Pin(reset_pin, Pin.OUT, value=1)
        self.a0 = Pin(a0_pin, Pin.OUT, value=0)
        
        # LEDピンはオプショナル（3V3接続の場合は不要）
        if led_pin is not None:
            self.led = Pin(led_pin, Pin.OUT, value=0)
        else:
            self.led = None
        
        self.width = width
        self.height = height
        self._base_width = width
        self._base_height = height
        self.rotation = 0  # 0, 1, 2, 3 (0°, 90°, 180°, 270°)
        
        # 通常のSPIを使用（PIOのSPI実装は複雑なため）
        self.spi = SPI(0, baudrate=20000000, polarity=0, phase=0, 
                       sck=Pin(clk_pin), mosi=Pin(mosi_pin))
        
        # フレームバッファ（RGB565: 16ビットカラー）
        self.fb_buf = bytearray(width * height * 2)
        self.fb = framebuf.FrameBuffer(self.fb_buf, width, height, framebuf.RGB565)
        
        self._init_display()
    
    def _init_display(self):
        """ST7789ディスプレイ初期化シーケンス"""
        self.reset.value(0)
        time.sleep_ms(10)
        self.reset.value(1)
        time.sleep_ms(120)
        
        init_cmds = [
            (0x11, None),           # SLPOUT
            (0x3A, bytes([0x05])),  # COLMOD: 16-bit RGB565
            (0x36, bytes([0x00])),  # MADCTL: RGB mode
            (0x29, None),           # DISPON
        ]
        
        for cmd, data in init_cmds:
            self._send_command(cmd)
            if data:
                self._send_data(data)
            time.sleep_ms(10)
        
        # LEDピンが設定されている場合のみON
        if self.led is not None:
            self.led.value(1)
    
    def _send_command(self, cmd):
        """コマンド送信（A0=0）"""
        self.cs.value(0)
        self.a0.value(0)
        self.spi.write(bytes([cmd]))
        self.cs.value(1)
    
    def _send_data(self, data):
        """データ送信（A0=1）"""
        self.cs.value(0)
        self.a0.value(1)
        self.spi.write(data)
        self.cs.value(1)
    
    def _set_window(self, x1, y1, x2, y2):
        """描画ウィンドウを設定（CASET, RASET）"""
        # CASET: Column Address Set
        self._send_command(0x2A)
        self._send_data(bytes([x1 >> 8, x1 & 0xFF, x2 >> 8, x2 & 0xFF]))
        
        # RASET: Row Address Set
        self._send_command(0x2B)
        self._send_data(bytes([y1 >> 8, y1 & 0xFF, y2 >> 8, y2 & 0xFF]))
    
    def _write_memory(self, buffer):
        """フレームバッファの内容をディスプレイに送信"""
        # WRITE_MEMORY コマンド
        self._send_command(0x2C)
        # ピクセルデータをすべて送信
        self._send_data(buffer)
    
    def rotate(self, rotation):
        """
        ディスプレイの向きを変更
        rotation: 0(0°), 1(90°), 2(180°), 3(270°)
        """
        self.rotation = rotation % 4
        madctl_values = [0x00, 0x60, 0xC0, 0xA0]
        self._send_command(0x36)
        self._send_data(bytes([madctl_values[self.rotation]]))
        
        # 90°/270°では幅と高さが入れ替わるので、フレームバッファを作り直す
        if self.rotation in (1, 3):
            new_width, new_height = self._base_height, self._base_width
        else:
            new_width, new_height = self._base_width, self._base_height
        
        if new_width != self.width or new_height != self.height:
            self.width = new_width
            self.height = new_height
            self.fb_buf = bytearray(self.width * self.height * 2)
            self.fb = framebuf.FrameBuffer(self.fb_buf, self.width, self.height, framebuf.RGB565)
    
    def text(self, text, x, y, color=Color.BLACK, bg=Color.WHITE, scale=1):
        """
        テキストを描画してディスプレイに反映
        color: 文字色（デフォルト黒）
        bg: 背景色（デフォルト白）
        scale: 文字の倍率（1=標準、2=2倍など）
        """
        if scale == 1:
            # 標準サイズ：背景を塗ってから文字を描画
            if bg is not None:
                self.fb.fill_rect(x, y, len(text) * 8, 8, bg)
            self.fb.text(text, x, y, color)
        else:
            # 拡大描画：1文字ずつ8x8バッファに描画してスケーリングコピー
            for i, char in enumerate(text):
                char_x = x + i * 8 * scale
                temp_buf = bytearray(8 * 8 * 2)
                temp_fb = framebuf.FrameBuffer(temp_buf, 8, 8, framebuf.RGB565)
                temp_fb.fill(bg)
                temp_fb.text(char, 0, 0, color)
                
                # スケーリングして描画（文字色・背景色ともにそのままコピー）
                for py in range(8 * scale):
                    for px in range(8 * scale):
                        src_x = px // scale
                        src_y = py // scale
                        dst_x = char_x + px
                        dst_y = y + py
                        if dst_x < self.width and dst_y < self.height:
                            src_idx = (src_y * 8 + src_x) * 2
                            pixel_data = (temp_buf[src_idx + 1] << 8) | temp_buf[src_idx]
                            self.fb.pixel(dst_x, dst_y, pixel_data)
        
        # 描画した範囲のみ送信
        text_w = len(text) * 8 * scale
        text_h = 8 * scale
        self._refresh_region(x, y, text_w, text_h)
    
    def fill(self, color):
        """フレームバッファを指定色で塗りつぶし"""
        self.fb.fill(color)
        self.refresh()
    
    def rect(self, x, y, w, h, color):
        """矩形（枠線）を描画"""
        self.fb.rect(x, y, w, h, color)
        self._refresh_region(x, y, w, h)
    
    def fill_rect(self, x, y, w, h, color):
        """矩形を塗りつぶす"""
        self.fb.fill_rect(x, y, w, h, color)
        self._refresh_region(x, y, w, h)
    
    def pixel(self, x, y, color):
        """単一ピクセルを描画"""
        self.fb.pixel(x, y, color)
        self._refresh_region(x, y, 1, 1)
    
    def line(self, x1, y1, x2, y2, color):
        """線を描画"""
        self.fb.line(x1, y1, x2, y2, color)
        min_x = min(x1, x2)
        min_y = min(y1, y2)
        w = abs(x2 - x1) + 1
        h = abs(y2 - y1) + 1
        self._refresh_region(min_x, min_y, w, h)
    
    def refresh(self):
        """フレームバッファ全体をディスプレイに反映"""
        self._set_window(0, 0, self.width - 1, self.height - 1)
        self._write_memory(self.fb_buf)
    
    def _refresh_region(self, x, y, w, h):
        """フレームバッファの指定矩形領域のみをディスプレイに反映"""
        # 画面範囲にクリップ
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.width - 1, x + w - 1)
        y1 = min(self.height - 1, y + h - 1)
        
        if x0 > x1 or y0 > y1:
            return
        
        region_w = x1 - x0 + 1
        region_h = y1 - y0 + 1
        
        # フレームバッファから対象領域を抽出
        region_buf = bytearray(region_w * region_h * 2)
        stride = self.width * 2
        for row in range(region_h):
            src_offset = (y0 + row) * stride + x0 * 2
            dst_offset = row * region_w * 2
            region_buf[dst_offset:dst_offset + region_w * 2] = self.fb_buf[src_offset:src_offset + region_w * 2]
        
        self._set_window(x0, y0, x1, y1)
        self._write_memory(region_buf)
    
    def draw_image(self, image_data, x, y, img_width, img_height):
        """
        RGB565形式の画像を指定座標に描画
        image_data: RGB565形式のバイト配列（幅×高さ×2バイト）
        x, y: 描画開始座標（左上）
        img_width, img_height: 画像の幅と高さ
        """
        # 画面範囲外の場合は何もしない
        if x >= self.width or y >= self.height:
            return
        if x + img_width <= 0 or y + img_height <= 0:
            return
        
        # クリッピング計算
        src_x_start = 0
        src_y_start = 0
        dst_x_start = x
        dst_y_start = y
        copy_width = img_width
        copy_height = img_height
        
        # 左端クリッピング
        if x < 0:
            src_x_start = -x
            dst_x_start = 0
            copy_width += x
        
        # 上端クリッピング
        if y < 0:
            src_y_start = -y
            dst_y_start = 0
            copy_height += y
        
        # 右端クリッピング
        if dst_x_start + copy_width > self.width:
            copy_width = self.width - dst_x_start
        
        # 下端クリッピング
        if dst_y_start + copy_height > self.height:
            copy_height = self.height - dst_y_start
        
        # 有効範囲チェック
        if copy_width <= 0 or copy_height <= 0:
            return
        
        # フレームバッファに画像データをコピー
        fb_stride = self.width * 2
        img_stride = img_width * 2
        
        for row in range(copy_height):
            src_y = src_y_start + row
            dst_y = dst_y_start + row
            
            src_offset = src_y * img_stride + src_x_start * 2
            dst_offset = dst_y * fb_stride + dst_x_start * 2
            
            self.fb_buf[dst_offset:dst_offset + copy_width * 2] = \
                image_data[src_offset:src_offset + copy_width * 2]
        
        # 描画した領域を画面に反映
        self._refresh_region(dst_x_start, dst_y_start, copy_width, copy_height)
    
    def draw_image_file(self, filename, x, y, img_width, img_height):
        """
        外部ファイルからRGB565形式の画像を読み込んで描画
        filename: RGB565 raw形式の画像ファイルパス
        x, y: 描画開始座標（左上）
        img_width, img_height: 画像の幅と高さ
        
        使用方法：
        1. PC側でPythonなどで画像をRGB565 raw形式に変換
        2. ファイルをPicoに転送
        3. このメソッドで読み込んで描画
        """
        try:
            with open(filename, 'rb') as f:
                image_data = f.read()
                expected_size = img_width * img_height * 2
                
                if len(image_data) < expected_size:
                    print(f"警告: ファイルサイズが不足 (期待:{expected_size}, 実際:{len(image_data)})")
                    return
                
                self.draw_image(image_data, x, y, img_width, img_height)
        except OSError as e:
            print(f"エラー: ファイル '{filename}' を読み込めません: {e}")


class Button:
    """GNDに落ちるボタン（ACTIVE_LOW）"""
    def __init__(self, pin_num):
        self.pin = Pin(pin_num, Pin.IN, Pin.PULL_UP)
        self.pressed_time = None
        self.sent = False
    
    def is_pressed(self):
        return self.pin.value() == 0
    
    def update(self):
        """状態を更新"""
        if self.is_pressed():
            if self.pressed_time is None:
                self.pressed_time = time.ticks_ms()
        else:
            self.pressed_time = None
            self.sent = False
    
    def held_for(self, seconds):
        """指定秒数以上押されているか"""
        if self.pressed_time is None:
            return False
        elapsed = time.ticks_diff(time.ticks_ms(), self.pressed_time)
        return elapsed >= seconds * 1000 and not self.sent
