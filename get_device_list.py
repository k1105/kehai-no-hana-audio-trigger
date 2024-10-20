import time
import hmac
import hashlib
import base64
import uuid

# APIトークンとシークレットキーを設定
token = "9aa633e8abbd5942aaffba16b72a932788ab5334781ee687b8b9632d9558ca7b079b5a26138e68ead170b5f8619436ad"
secret = "4fe045e05906ea2141a293ccf7904232"

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
