# import whisper
# import sounddevice as sd
# import numpy as np
# import scipy.io.wavfile as wav
# import tempfile

# # Load the Whisper model
# model = whisper.load_model("base")  # You can use 'tiny', 'small', etc. for speed/accuracy tradeoff

# def record_audio(duration=5, fs=16000):
#     print("🎙️ Listening...")
#     recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
#     sd.wait()
#     return recording, fs

# def transcribe_audio():
#     audio, fs = record_audio()
    
#     # Save to a temporary file
#     with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
#         wav.write(f.name, fs, audio)
#         print("🧠 Transcribing...")
#         result = model.transcribe(f.name, fp16=False)
    
#     print("🗣️ You said:", result["text"])
#     return result["text"]

# # Example usage
# if __name__ == "__main__":
#     while True:
#         try:
#             text = transcribe_audio()
#             # Optional: modify, translate, or classify the query
#         except KeyboardInterrupt:
#             print("\n🔚 Stopped.")
#             break

import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer
import numpy as np
import wave
import whisper
import tempfile
import os

# Load Whisper model for final transcription
whisper_model = whisper.load_model("base")

# Initialize Vosk model (download and extract first!)
vosk_model = Model("D:/Applications/Application Reinstaller/vosk-model-small-en-us-0.15")

samplerate = 16000
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print("⚠️", status)
    q.put(bytes(indata))

def record_until_done():
    print("🎙️ Speak now (listening until you're done)...")
    rec = KaldiRecognizer(vosk_model, samplerate)
    rec.SetWords(True)

    recorded_data = []

    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                break  # Detected end of speech
            recorded_data.append(data)

    print("🛑 Speech ended.")
    return b''.join(recorded_data)

def save_audio(raw_audio_bytes, filename="temp_audio.wav"):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(raw_audio_bytes)
    return filename

def transcribe_with_whisper(filepath):
    print("🧠 Transcribing with Whisper...")
    result = whisper_model.transcribe(filepath, fp16=False)
    print("🗣️ You said:", result["text"])
    return result["text"]

# Main loop
if __name__ == "__main__":
    while True:
        try:
            raw_audio = record_until_done()
            wav_path = save_audio(raw_audio)
            transcribe_with_whisper(wav_path)
            os.remove(wav_path)
        except KeyboardInterrupt:
            print("\n🔚 Stopped.")
            break
