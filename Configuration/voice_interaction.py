import speech_recognition as sr
import pyttsx3

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

def talk(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
