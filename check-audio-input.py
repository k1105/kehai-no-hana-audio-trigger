import pyaudio

pa = pyaudio.PyAudio()

print("デバイスの一覧:")
for i in range(pa.get_device_count()):
    info = pa.get_device_info_by_index(i)
    print(f"インデックス: {i}, 名前: {info['name']}, 入力チャンネル数: {info['maxInputChannels']}")
