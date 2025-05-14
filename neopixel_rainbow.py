import board
import neopixel_spi
import time

# 設定
num_pixels = 24    # LEDの数
pixels = neopixel_spi.NeoPixel_SPI(board.SPI(), num_pixels)

# HSVからRGBへの変換関数
def hsv2rgb(h, s, v):
    i = int(h * 6)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    i = i % 6

    if i == 0:
        r, g, b = v, t, p
    elif i == 1:
        r, g, b = q, v, p
    elif i == 2:
        r, g, b = p, v, t
    elif i == 3:
        r, g, b = p, q, v
    elif i == 4:
        r, g, b = t, p, v
    else:  # i == 5
        r, g, b = v, p, q

    return (int(r * 255), int(g * 255), int(b * 255))

# レインボーを移動させる
h_offset = 0
try:
    while True:
        # neo.clear_strip()
        pixels.fill((0,0,0))
        for i in range(num_pixels):
            h = (i + h_offset) / num_pixels  # 色相を移動させる
            r, g, b = hsv2rgb(h, 1, 0.2)     # HSVをRGBにする
            # neo.set_led_color(i, r, g, b)  # RGBに変換してセット
            pixels[i] = r, g, b
        # neo.update_strip()  # 更新
#        pixels.write()
        h_offset += 1  # オフセットを更新（レインボーが移動）
        time.sleep(0.01)  # 少し待機

except KeyboardInterrupt:
    print("stop")
    #neo.clear_strip()
    #neo.update_strip()
    pixels.fill((0,0,0))
#    pixels.write()
