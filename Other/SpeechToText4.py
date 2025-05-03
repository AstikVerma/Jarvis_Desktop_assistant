# import speech_recognition

# def takeCommand():
#     r = speech_recognition.Recognizer()
#     with speech_recognition.Microphone() as source:
#         print("Listening.....")
#         r.pause_threshold = 1
#         r.energy_threshold = 300
#         audio = r.listen(source,0,4)

#     try:
#         print("Understanding..")
#         query  = r.recognize_google(audio,language='en-in')
#         print(f"You Said: {query}\n")
#     except Exception as e:
#         print("Say that again")
#         return "None"
#     return query

# if __name__ == "__main__":
#     while True:
#         query = takeCommand().lower()
#         print(query)


import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone()

def callback(recognizer, audio):
    try:
        text = recognizer.recognize_google(audio)
        print("Heard:", text)
    except sr.UnknownValueError:
        print("Didn't catch that.")
    except sr.RequestError as e:
        print(f"API error: {e}")

# Adjust for ambient noise (important!)
with mic as source:
    print("Calibrating mic...")
    r.adjust_for_ambient_noise(source, duration=1)

# Start background listening
print("Listening...")
stop_listening = r.listen_in_background(mic, callback)

# Keep the program alive (or do other stuff)
import time
while True:
    time.sleep(0.1)
