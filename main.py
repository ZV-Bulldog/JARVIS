import threading  # To handle timeout for user responses
import os  # To interact with the operating system
import keyboard  # To detect keypresses (like the 'J' key)
import sys  # To exit the program
import pyttsx3 
from Modules.wake_word import listen_for_wake_word  # Wake word detection
from Modules.assistant import execute_command  # Command execution functionality
from Configuration.voice_interaction import take_command, talk  # Voice interaction functions
from conversation_handler import save_conversation, periodic_chunking  # Conversation handling

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

# Constants and Global Variables
SHUTDOWN_KEYWORDS = ["shut down", "quit", "stop", "go to sleep", "ultron is coming"]
MAX_RETRIES = 3  # Maximum number of retries before stopping
TIMEOUT_SECONDS = 5  # Time to wait for a user command before timing out
shutdown_flag = False  # Flag to control the assistant's running state

def timeout_function():
    """Triggered after a timeout period to return an empty string if no input is detected."""
    return ""

def take_command_with_timeout():
    """
    Listen for the user's voice command with a timeout.
    If no command is received within the timeout period, returns an empty string.
    """
    timer = threading.Timer(TIMEOUT_SECONDS, timeout_function)
    timer.start()
    
    command = take_command().strip().lower()  # Capture and normalize user input
    timer.cancel()  # Cancel the timer if a command is received
    
    return command

def process_command(command):
    """
    Process the given command: execute it and save the conversation.
    """
    assistant_response = execute_command(command)  # Process the command
    save_conversation(command, assistant_response)  # Save conversation details
    periodic_chunking()  # Periodically summarize and chunk conversations

def handle_shutdown():
    """
    Safely shut down the assistant, confirming the action with the user.
    """
    global shutdown_flag
    shutdown_flag = True
    talk("Shutting down, Sir.")  # Notify the user
    print("Assistant is shutting down...")  # Log shutdown

def retry_user_command(retry_count):
    """
    Retry user input if no command is detected.
    """
    if retry_count < MAX_RETRIES:
        talk("I didn't hear you, Mr. Vickers. Say that again.")  # Prompt the user
        print(f"Retry {retry_count + 1}/{MAX_RETRIES}: Listening for command...")  # Log retry status
        return retry_count + 1  # Increment retry count
    else:
        talk("I'm sorry, Sir, I have to stop now.")  # Final prompt after max retries
        print("Max retries reached. Shutting down.")  # Log shutdown
        return MAX_RETRIES  # Indicate max retries reached

def stop_speaking():
    """Function to stop talking and exit the program when 'J' is pressed."""
    print("J key pressed! Stopping speech and exiting...")
    engine.stop()  # Stop the speech immediately

def main():
    """
    Main loop to manage the virtual assistant's functionality: listen for commands, 
    process them, handle retries, and manage shutdown.
    """
    global shutdown_flag
    retry_count = 0  # Counter to track retries

    # Add the hotkey listener for the 'J' key to stop speech
    keyboard.add_hotkey('j', stop_speaking)

    try:
        while not shutdown_flag:
            if retry_count == 0:  # On first attempt, wait for the wake word
                print("Listening for wake word...")
                listen_for_wake_word()  # Block until wake word is detected

            # Wake word detected, now listen for the user's command
            print("Wake word detected!")
            command = take_command_with_timeout()  # Get the command with a timeout

            if not command:  # No command was received
                retry_count = retry_user_command(retry_count)  # Retry or stop after max retries
                if retry_count >= MAX_RETRIES:  # Stop after max retries
                    break
                continue  # Continue listening for commands

            # Check for shutdown commands
            if any(keyword in command for keyword in SHUTDOWN_KEYWORDS):
                handle_shutdown()
                break

            # If command is valid, process and reset retry counter
            if command:
                process_command(command)
                retry_count = 0  # Reset retry count after successful command

    except KeyboardInterrupt:
        print("Assistant manually terminated.")  # Log termination on manual interrupt

# Start the assistant if this script is run directly
if __name__ == "__main__":
    main()
