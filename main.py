import os
from os.path import join, dirname
from dotenv import load_dotenv
import time
import hmac
import hashlib
import base64
import uuid
import requests
import speech_recognition as sr
from google.cloud import speech

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# APIトークンとシークレットキーを設定
token = os.environ.get("TOKEN")
secret = os.environ.get("SECRET")
device_id = "D03534382360"  # 山岸ボタンのデバイスID

# 音声認識の設定
recognizer = sr.Recognizer()
mic = sr.Microphone()

# Google Cloud Speech-to-Text クライアントの初期化
client = speech.SpeechClient()

# 署名を生成する関数
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

# SwitchBotのボタンを押す関数
def press_button():
    url = f"https://api.switch-bot.com/v1.1/devices/{device_id}/commands"
    headers = generate_signature()
    payload = {
        "command": "press",  # ボタンを押す動作
        "parameter": "default",
        "commandType": "command"
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("山岸ボタンを押しました。")
    else:
        print(f"エラー: {response.status_code}, メッセージ: {response.text}")

# 音声認識とボタン操作を連動させる関数
def transcribe_and_control():
    while True:
        with mic as source:
            print("マイクからの入力を待っています...")
            recognizer.adjust_for_ambient_noise(source)
            try:
                # スピーチを録音して文字起こし
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=10)
                response = client.recognize(
                    config={
                        "encoding": speech.RecognitionConfig.AudioEncoding.LINEAR16,
                        "sample_rate_hertz": 48000,
                        "language_code": "ja-JP",
                    },
                    audio={"content": audio.get_wav_data()},
                )

                # 認識結果を取得
                for result in response.results:
                    transcript = result.alternatives[0].transcript
                    print(f"認識結果: {transcript}")

                    # フレーズに応じてSwitchBotを操作
                    if any(phrase in transcript for phrase in ["おはよう", "いってきます", "ただいま"]):
                        print(f"{transcript}が検出されました。山岸ボタンを操作します。")
                        press_button()

            except sr.WaitTimeoutError:
                print("無音が続いています。")
            except Exception as e:
                print(f"エラーが発生しました: {e}")

# 実行
transcribe_and_control()
