from gpiozero import PWMLED
import time
import math

def ease_in_out(t):
    """Ease-in-out関数 (sinカーブを使用)"""
    return 0.5 * (1 - math.cos(math.pi * t))

def smooth_blink(led, duration, steps=100):
    """
    LEDを滑らかに点灯/消灯させる。
    :param led: PWMLEDインスタンス
    :param duration: 明滅にかける時間 (秒)
    :param steps: 明るさを変化させるステップ数
    """
    step_duration = duration / steps
    for i in range(steps + 1):
        t = i / steps
        brightness = ease_in_out(t)
        led.value = brightness
        time.sleep(step_duration)
    
    for i in range(steps + 1):
        t = i / steps
        brightness = ease_in_out(1 - t)
        led.value = brightness
        time.sleep(step_duration)
