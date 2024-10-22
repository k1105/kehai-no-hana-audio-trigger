#!bin/bash
cd $HOME/Desktop/kehai-no-hana-audio-trigger
python -m venv myenv
sudo apt-get update
source myenv/bin/activate
sudo apt-get install libportaudio2 libportaudiocpp0 portaudio19-dev python3-dev
pip install -r requirements.txt