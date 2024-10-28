#!bin/bash
cd $HOME/Desktop/kehai-no-hana-audio-trigger
python -m venv myenv --system-site-packages
sudo apt-get update
source myenv/bin/activate
sudo apt-get install libportaudio2 libportaudiocpp0 portaudio19-dev python3-dev
pip install -r requirements.txt
mv audio-trigger.service /etc/systemd/system/audio-trigger.service
sudo systemctl daemon-reload