# import pyttsx3
# import pygame
# import random
# import os
# import threading
# from dotenv import dotenv_values

# # Load environment variables
# env_vars = dotenv_values(".env")
# AssistantVoice = env_vars.get("AssistantVoice", None)

# #David, Hazel, Linda, mark, richard, George

# # Initialize pyttsx3 engine
# engine = pyttsx3.init()
# voices = engine.getProperty('voices')

# # Attempt to match voice if specified
# if AssistantVoice:
#     for voice in voices:
#         if AssistantVoice.lower() in voice.id.lower():
#             engine.setProperty('voice', voice.id)
#             break

# # engine.setProperty('voice', 1)

# # Optional rate and pitch adjustment (you can tweak here)
# engine.setProperty('rate', 180)

# def generate_tts_pyttsx3(text, output_file):
#     try:
#         engine.save_to_file(text, output_file)
#         engine.runAndWait()
#         print("\033[92mTTS saved successfully.\033[0m")
#     except Exception as e:
#         print(f"\033[91mError generating TTS: {e}\033[0m")

# def play_audio(file_path):
#     pygame.mixer.init()
#     pygame.mixer.music.load(file_path)
#     pygame.mixer.music.play()
#     while pygame.mixer.music.get_busy():
#         pygame.time.Clock().tick(10)
#     pygame.mixer.quit()

# def remove_file(file_path):
#     try:
#         if os.path.exists(file_path):
#             os.remove(file_path)
#             print(f"Removed file: {file_path}")
#     except Exception as e:
#         print(f"Error removing file: {e}")

# def TTS(text, func=lambda r=None: True):
#     file_path = "output.wav"
#     generate_tts_pyttsx3(text, file_path)
#     if os.path.exists(file_path):
#         play_audio(file_path)
#     remove_file(file_path)

# def TextToSpeech(text, func=lambda x=None: True):
#     Data = str(text).split(".")
#     responses = [
#         "The rest of the result has been printed to the chat screen, kindly check it out sir.",
#         "Sir, you'll find more text on the chat screen for you to see.",
#         "You can see the rest of the text on the chat screen, sir.",
#         "Sir, please look at the chat screen, the rest of the answer is there.",
#         "Sir, take a look at the chat screen for additional text.",
#         "You'll find the complete answer on the chat screen, kindly check it out sir.",
#     ]
#     if len(Data) > 4 and len(text) > 250:
#         TTS(" ".join(text.split(".")[0:2]) + ". " + random.choice(responses), func)
#     else:
#         TTS(text, func)

# def speak(text):
#     tts_thread = threading.Thread(target=TTS, args=(text,))
#     tts_thread.start()
#     tts_thread.join()

# # Main
# if __name__ == "__main__":
#     while True:
#         try:
#             TextToSpeech(input("Enter the text: "))
#         except KeyboardInterrupt:
#             print("\nExiting...")
#             break
import pyttsx3
from dotenv import dotenv_values

def TextToSpeech(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)

    env_vars = dotenv_values(".env")
    AssistantVoice = env_vars.get("AssistantVoice", None)

    voices = engine.getProperty('voices')
    if AssistantVoice:
        for voice in voices:
            if AssistantVoice.lower() in voice.id.lower():
                engine.setProperty('voice', voice.id)
                break

    print(f"[TTS]: Speaking: {text}")
    engine.say(text)
    engine.runAndWait()
    
if __name__ == "__main__":
    while True:
        try:
            TextToSpeech(input("Enter the text: "))
        except KeyboardInterrupt:
            print("\nExiting...")
            break