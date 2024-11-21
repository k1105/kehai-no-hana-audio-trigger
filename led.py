from gpiozero import LED
import time

# GPIO17に接続されたLEDのインスタンス作成
led = LED(17)

# 音声認識と連動してSwitchBotを操作し、LEDを点灯させる
def turn_on_led():
    led.on()  # LEDを点灯
    time.sleep(1)  # 1秒間点灯
    led.off()  # LEDを消灯

# 実行
turn_on_led()
