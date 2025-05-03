# merged_voice_assistant.py

# Importing functions from texttospeech.py and speechtotext.py
from TextToSpeech import TextToSpeech  # Assuming this is where TextToSpeech is defined
from SpeechToText import SpeechRecognition, UniversalTranslator, QueryModifier, SetAssistantStatus, InputLanguage

def main():
    while True:
        try:
            # Listen for speech and convert to text
            print("Listening for input...")
            text = SpeechRecognition()

            # Modify or translate the query based on input language
            if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
                response = QueryModifier(text)
            else:
                SetAssistantStatus('Translating ...')
                response = QueryModifier(UniversalTranslator(text))

            # Print and speak the modified/translated response
            print(f"Response: {response}")
            TextToSpeech(response)

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

if __name__ == "__main__":
    main()
