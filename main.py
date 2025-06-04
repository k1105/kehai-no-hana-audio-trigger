import time
import os
from os.path import join, dirname
from dotenv import load_dotenv
import hmac
import hashlib
import base64
import uuid
import requests
import speech_recognition as sr
from google.cloud import speech

# from gpiozero import PWMLED
# from led_utils import smooth_blink  # 外部モジュールから関数をインポート

# GPIO17に接続されたLEDのインスタンス作成
# led = PWMLED(17)

# 環境変数をロード
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

token = os.environ.get("TOKEN")
secret = os.environ.get("SECRET")
device_id = os.environ.get("DEVICE_ID")

recognizer = sr.Recognizer()
mic = sr.Microphone()

client = speech.SpeechClient()

def generate_signature():
    t = int(round(time.time() * 1000))
    nonce = uuid.uuid4()
    string_to_sign = f"{token}{t}{nonce}"
    sign = base64.b64encode(hmac.new(secret.encode(), string_to_sign.encode(), hashlib.sha256).digest()).decode().upper()
    return {
        "Authorization": token,
        "sign": sign,
        "t": str(t),
        "nonce": str(nonce),
        "Content-Type": "application/json"
    }

def press_button():
    url = f"https://api.switch-bot.com/v1.1/devices/{device_id}/commands"
    headers = generate_signature()
    payload = {
        "command": "press",
        "parameter": "default",
        "commandType": "command"
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("ボット77を押しました。")
    else:
        print(f"エラー: {response.status_code}, メッセージ: {response.text}")

# 音声認識と連動してSwitchBotを操作し、LEDを点灯させる
def transcribe_and_control():
    while True:
        with mic as source:
            print("マイクからの入力を待っています...")
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=10)
                response = client.recognize(
                    config={
                        "encoding": speech.RecognitionConfig.AudioEncoding.LINEAR16,
                        "sample_rate_hertz": 48000,
                        "language_code": "ja-JP",
                    },
                    audio={"content": audio.get_wav_data()},
                )

                for result in response.results:
                    transcript = result.alternatives[0].transcript
                    print(f"認識結果: {transcript}")

                    if any(phrase in transcript for phrase in ["おはよう", "いってきます", "行ってきます", "ただいま"]):
                        print(f"{transcript}が検出されました。ボット77を操作し、LEDを点灯します。")
                        press_button()
                        # smooth_blink(led, duration=1)  # 1秒間で明滅

            except sr.WaitTimeoutError:
                print("無音が続いています。")
            except Exception as e:
                print(f"エラーが発生しました: {e}")

# 実行
transcribe_and_control()
