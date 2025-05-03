# import requests

# url = "http://localhost:11434/api/generate"
# payload = {
#     "model": "gemma:2b",
#     # "model": "tinyllama",
#     # "prompt": "what is python",
#     "prompt": "what was number I told you to remeber just giveback that number",
#     "stream": False
# }

# response = requests.post(url, json=payload)
# if(response):
#     print(response.json()["response"])
# else:
#     print("No response")

##############################################################################################################################

# import whisper
# import sounddevice as sd
# import numpy as np
# import scipy.io.wavfile as wav

# def record_audio(duration=5, samplerate=16000):
#     print("🎙️ Recording...")
#     audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
#     sd.wait()
#     wav.write("test_audio.wav", samplerate, audio)
#     print("✅ Recording saved as test_audio.wav")

# def transcribe_audio():
#     model = whisper.load_model("base")  # or "small", "medium", "large"
#     result = model.transcribe("test_audio.wav", fp16=False)
#     print("📝 Transcription:", result["text"])

# record_audio()
# transcribe_audio()



###########################################################################################################################
# Get Voices present in Windows
# import pyttsx3

# engine = pyttsx3.init()
# voices = engine.getProperty('voices')

# print(f"Total voices found: {len(voices)}")
# for i, voice in enumerate(voices):
#     print(f"{i}: {voice.name} - {voice.id}")

#############################################################################################################################
# Voice Audition 

# import pyttsx3
# import os

# # Text to be saved in each voice
# paragraph = """
# Good morning, sir. I hope you're doing well today. 
# Your calendar is clear for the next few hours, but you do have a meeting scheduled at 3 PM. 
# The weather outside is pleasant — 24 degrees with a light breeze, perfect for a walk. 
# Also, I’ve gone ahead and updated your project folder with the latest files. 
# Let me know if you'd like me to read out the summary or open any document for you. I'm here to assist.
# """

# # Folder to store audio files
# output_folder = "Other/audition"
# os.makedirs(output_folder, exist_ok=True)

# def sanitize_filename(name):
#     return "".join(c for c in name if c.isalnum() or c in (" ", "_", "-")).rstrip()

# def save_voice_audios(text):
#     engine = pyttsx3.init()
#     voices = engine.getProperty('voices')
    
#     print(f"\n🔈 Saving audio for {len(voices)} voices...\n")

#     for index, voice in enumerate(voices):
#         voice_name = sanitize_filename(voice.name)
#         file_path = os.path.join(output_folder, f"{voice_name}.mp3")

#         if os.path.exists(file_path):
#             print(f"✅ Skipping (already exists): {voice_name}")
#             continue

#         try:
#             print(f"💾 Saving voice {index}: {voice_name}")
#             engine.setProperty('voice', voice.id)
#             engine.save_to_file(text, file_path)
#             engine.runAndWait()
#         except Exception as e:
#             print(f"❌ Error with {voice_name}: {e}")

#     engine.stop()
#     print("\n🎉 All voice files saved successfully!")

# if __name__ == "__main__":
#     save_voice_audios(paragraph)


#########################################################################################################################
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# def BingSearch(query):
#     options = Options()
#     options.add_argument("--headless")
#     options.add_argument("--disable-gpu")
#     options.add_argument("--no-sandbox")
#     options.add_argument("user-agent=Mozilla/5.0")

#     driver = webdriver.Chrome(options=options)
#     driver.get(f"https://www.bing.com/search?q={query}")

#     try:
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.b_algo"))
#         )
#         results = driver.find_elements(By.CSS_SELECTOR, "li.b_algo")[:4]

#         Answer = f"The search results for '{query}' are:\n[start]\n"
#         for i, result in enumerate(results, 1):
#             title = result.find_element(By.TAG_NAME, "h2").text
#             link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
#             Answer += f"{i}. {title}\n{link}\n\n"

#         Answer += "[end]"
#     except Exception as e:
#         Answer = f"[ERROR] {e}\n[start]\n[end]"

#     driver.quit()
#     return Answer

# print(BingSearch("who is mahatma gandhi"))

from googlesearch import search
def GoogleSearch(query):
    results = list(search(query))
    Answer = f"The search results for '{query}' are:\n[start]\n"
    print(results)
    for i in results:
        # Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"
    
        Answer += "[end]"
    return Answer
GoogleSearch("What is mahatma gandhi")

