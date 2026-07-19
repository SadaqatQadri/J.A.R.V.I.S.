import pyaudio
import numpy as np
from openwakeword.model import Model

def wait_for_wake_word():
    print(">>> wait_for_wake_word() function STARTED", flush=True)
    owwModel = Model(wakeword_models=["hey_jarvis"], inference_framework="onnx")
    print(">>> Model loaded successfully", flush=True)

    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=16000,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=1280
    )

    print("Waiting for wake word 'Hey Jarvis'...", flush=True)

    try:
        for _ in range(20):
            audio_chunk = np.frombuffer(stream.read(1280, exception_on_overflow=False), dtype=np.int16)
            owwModel.predict(audio_chunk)

        while True:
            audio_chunk = np.frombuffer(stream.read(1280, exception_on_overflow=False), dtype=np.int16)
            prediction = owwModel.predict(audio_chunk)
            score = prediction["hey_jarvis"]
            print(f"score: {score:.3f}", flush=True)

            if score > 0.5:
                print("Wake word detected!", flush=True)
                break
    finally:
        stream.close()
        pa.terminate()

if __name__ == "__main__":
    wait_for_wake_word()