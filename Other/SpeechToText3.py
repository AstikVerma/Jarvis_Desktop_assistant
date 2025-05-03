import speech_recognition as sr
import pyttsx3

# Initialize the recognizer
r = sr.Recognizer()

# Function to convert text to speech
def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    
    # Set properties like rate, volume (optional)
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)
    
    engine.say(command)
    engine.runAndWait()

# Loop infinitely for user to speak
while True:
    try:
        # Use the microphone as the source for input
        with sr.Microphone() as source2:
            # Adjust for ambient noise
            r.adjust_for_ambient_noise(source2, duration=1)
            
            # Listen for the user's input
            print("Listening...")  # Optionally print listening message
            audio2 = r.listen(source2)
            
            # Use Google to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
            
            print(f"Did you say: {MyText}")
            SpeakText(MyText)

            # Exit condition for stopping the program (example: "exit")
            if "exit" in MyText:
                print("Exiting...")
                break

    except sr.RequestError as e:
        print(f"Could not request results; {e}")
    
    except sr.UnknownValueError:
        print("Unknown error occurred.")
