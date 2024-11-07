#!/bin/bash
cd /home/pi/Desktop/kehai-no-hana-audio-trigger/

# 環境変数の設定
export PULSE_SERVER=127.0.0.1
export ALSA_CONFIG_PATH=/etc/asound.conf
export PATH=$PATH:/usr/bin

# デバッグ情報の表示
echo "Activating virtual environment..."
source myenv/bin/activate
echo "Virtual environment activated."

which python
python --version

echo "Starting Python script..."
python main.py
echo "Python script finished with exit code $?"
