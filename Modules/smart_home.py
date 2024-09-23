from Configuration.voice_interaction import talk
from Configuration.config import OPENAI_API_KEY
import openai
from Services.openai_service import jarvis_rephrase

# Smart home device control
def control_device(command):
    if 'light' in command:
        if 'on' in command:
            response = jarvis_rephrase("Turning on the light.")
            print(response)
            talk(response)
            # Code to turn on the light
        elif 'off' in command:
            response = jarvis_rephrase("Turning off the light.")
            print(response)
            talk(response)
            # Code to turn off the light
    elif 'thermostat' in command:
        if 'set to' in command:
            temperature = int(command.split('set to')[-1].strip())
            response = jarvis_rephrase(f"Setting thermostat to {temperature} degrees.")
            print(response)
            talk(response)
            # Code to set the thermostat temperature
    else:
        talk(jarvis_rephrase("Device command not recognized."))