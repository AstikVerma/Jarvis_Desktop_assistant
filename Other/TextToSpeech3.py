from TTS.api import TTS
import os
import random
from dotenv import dotenv_values
import sounddevice as sd
import soundfile as sf

# Load environment variables
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice", "tts_models/en/ljspeech/tacotron2-DDC")  # default voice

# Initialize TTS model
tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")


def play_audio(file_path):
    data, samplerate = sf.read(file_path)
    sd.play(data, samplerate)
    sd.wait()

def remove_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Removed file: {file_path}")
    except Exception as e:
        print(f"Error removing file: {e}")

def generate_tts(text, output_file="output.wav"):
    try:
        tts.tts_to_file(text=text, file_path=output_file)
        print("\033[92mTTS saved successfully.\033[0m")
    except Exception as e:
        print(f"\033[91mError generating TTS: {e}\033[0m")

def speak_text(text):
    output_file = "output.wav"
    generate_tts(text, output_file)
    if os.path.exists(output_file):
        play_audio(output_file)
    remove_file(output_file)

def TextToSpeech(text):
    Data = str(text).split(".")
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "You can see the rest of the text on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
    ]
    if len(Data) > 4 and len(text) > 250:
        preview_text = " ".join(text.split(".")[0:2]) + ". " + random.choice(responses)
        speak_text(preview_text)
    else:
        speak_text(text)

if __name__ == "__main__":
    try:
        while True:
            TextToSpeech(input("Enter the text: "))
    except KeyboardInterrupt:
        print("\nExiting...")
