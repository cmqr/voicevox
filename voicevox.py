# PythonからVOICEVOXを実行する

import requests
import json
import sounddevice as sd
import numpy as np

# from rich import print


host = "127.0.0.1"
port = "50021"
speaker = 3


def post_audio_query(text: str) -> dict:
    # 音声合成用のクエリを作成する
    params = {"text": text, "speaker": speaker}

    res = requests.post(
        f"http://{host}:{port}/audio_query",
        params=params,
    )

    query_data = res.json()
    # query_data["speedScale"] = 1.5

    # print(query_data)

    return query_data


def post_synthesis(query_data: dict) -> bytes:
    # 音声合成を実行する
    params = {"speaker": speaker}
    headers = {"content-type": "application/json"}

    res = requests.post(
        f"http://{host}:{port}/synthesis",
        data=json.dumps(query_data),
        params=params,
        headers=headers,
    )

    return res.content


def play_wavfile(wav_data: bytes):
    # 音声を再生する
    sample_rate = 24000  # サンプリングレート
    wav_array = np.frombuffer(wav_data, dtype=np.int16)  # バイトデータをnumpy配列に変換
    sd.play(wav_array, sample_rate, blocking=True)  # 音声の再生


def text_to_voice():
    # 入力したテキストをVOICEVOXの音声で再生する
    while True:
        text = input("テキストを入力してください: ")
        if text == "q":
            exit()

        res = post_audio_query(text)
        wav = post_synthesis(res)
        play_wavfile(wav)


if __name__ == "__main__":
    text_to_voice()
