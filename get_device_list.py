import time
import hmac
import hashlib
import base64
import uuid
import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# APIトークンとシークレットキーを設定
token = os.environ.get("TOKEN")
secret = os.environ.get("SECRET")

# Unix時間（13桁）
t = int(round(time.time() * 1000))

# nonce（ランダムなUUID）
nonce = uuid.uuid4()

# 署名を生成
string_to_sign = f"{token}{t}{nonce}"
sign = base64.b64encode(hmac.new(secret.encode(), string_to_sign.encode(), hashlib.sha256).digest()).decode().upper()

# 認証ヘッダーを作成
headers = {
    "Authorization": token,
    "sign": sign,
    "t": str(t),
    "nonce": str(nonce),
    "Content-Type": "application/json"
}

# リクエスト例（デバイスリストを取得）
import requests
response = requests.get("https://api.switch-bot.com/v1.1/devices", headers=headers)

print(response.json())
