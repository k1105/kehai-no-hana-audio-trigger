from gpiozero import PWMLED
from led_utils import smooth_blink  # smooth_blinkを外部ファイルからインポート
import time

# GPIO17に接続されたLEDのインスタンス作成
led = PWMLED(17)

# 1分周期でsmooth_blinkを実行
try:
    while True:
        smooth_blink(led, duration=1)  # 1秒間で明滅
        time.sleep(29)  # 1分 - 1秒の残りの時間待機
except KeyboardInterrupt:
    print("プログラムを終了します。")
    led.off()  # LEDを消灯
