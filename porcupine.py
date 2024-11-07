# from gpiozero import LED
import time
import os
from os.path import join, dirname
from dotenv import load_dotenv
import hmac
import hashlib
import base64
import uuid
import requests
import pvporcupine
import pyaudio
import struct

# GPIO17に接続されたLEDのインスタンス作成
# led = LED(17)

# 環境変数をロード
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

token = os.environ.get("TOKEN")
secret = os.environ.get("SECRET")
accesskey = os.environ.get("ACCESSKEY")
device_id = "D03534382360"

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
        print("山岸ボタンを押しました。")
    else:
        print(f"エラー: {response.status_code}, メッセージ: {response.text}")

# Porcupineの初期化
porcupine = pvporcupine.create(
    access_key=accesskey,
    keyword_paths=["ppn/ohayou_ja_mac_v3_0_0.ppn", "ppn/ittekimasu_ja_mac_v3_0_0.ppn", "ppn/tadaima_ja_mac_v3_0_0.ppn"],  # カスタムキーワードのパス
    model_path="pv/porcupine_params_ja.pv" 
)

# PyAudioの初期化
pa = pyaudio.PyAudio()

audio_stream = pa.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length)

def listen_and_control():
    try:
        print("キーワードを待機しています...")
        while True:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                if keyword_index==0:
                    print("おはよう")
                elif keyword_index==1:
                    print("行ってきます")
                else:
                    print("ただいま")
                print("キーワードが検出されました。山岸ボタンを操作し、LEDを点灯します。")
                press_button()
                # led.on()
                # time.sleep(1)
                # led.off()
    except KeyboardInterrupt:
        print("終了します。")
    finally:
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()
        if porcupine is not None:
            porcupine.delete()

# 実行
listen_and_control()
