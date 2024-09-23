import pvporcupine
import pyaudio
import numpy as np
from Configuration.config import PICOVOICE_ACCESS_KEY
from Configuration.voice_interaction import talk  # Import the talk function

def listen_for_wake_word():
    porcupine = pvporcupine.create(
        access_key=PICOVOICE_ACCESS_KEY,
        keywords=["jarvis"]
    )
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = np.frombuffer(pcm, dtype=np.int16)
        keyword_index = porcupine.process(pcm)
        if keyword_index >= 0:
            talk("Hello Sir")  # Say a greeting when the wake word is detected
            break
