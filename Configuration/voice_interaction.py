import speech_recognition as sr
import pyttsx3
from Configuration.config import ASSISTANT_IDENTITY

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            command = command.lower()
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            command = ""
        except sr.RequestError:
            print("Sorry, there was a problem with the speech recognition service.")
            command = ""
    return command

#def talk(text):
    #engine = pyttsx3.init()
    #engine.say(text)
    #engine.runAndWait()

def talk(text, voice_id=None):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    # Set the desired voice using the voice_id or fallback to a default
    if voice_id is not None:
        engine.setProperty('voice', voice_id)
    else:
        # You can set the default voice here by selecting from the list
        engine.setProperty('voice', voices[0].id)  # Use the first available voice by default
    # Slow down the speaking rate (default is around 200)
    rate = engine.getProperty('rate')  # Get the current rate
    engine.setProperty('rate', 192)  # Decrease rate by 50 (adjust as needed)
    engine.say(text)
    engine.runAndWait()

def explain_virtual_assistant():
    """Explains who the virtual assistant is."""
    talk(ASSISTANT_IDENTITY)  # Use the variable from config.py
    print(ASSISTANT_IDENTITY)  # Log the response
