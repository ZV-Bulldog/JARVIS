import openai
import logging
from Services.serpapi_service import get_news, get_weather, search_web
from Services.wolframalpha_service import calculate
from Modules.smart_home import control_device
from Configuration.voice_interaction import talk
from Configuration.config import GREETING, USER_NAME, USER_TITLE, PERSONALITY, OPENAI_API_KEY
from Services.openai_service import get_chatgpt_response

# Configure logging for debugging
logging.basicConfig(level=logging.INFO)

# Initialize OpenAI with your API key
openai.api_key = OPENAI_API_KEY

# Define Global Variables
CALCULATION_KEYWORDS = ['calculate', 'compute', 'evaluate', 'solve']
SEARCH_KEYWORDS = ['search', 'look up']

def execute_command(command):
    """Execute the appropriate function based on the user command."""
    command = command.lower().strip()  # Normalize and clean up the command

    # Weather-related command
    if 'weather' in command:
        get_weather()
        return  # Exit early if weather info is processed

    # News-related command
    elif 'news' in command:
        if 'top news' in command:
            get_news("top news")  # If 'top news' is specified, set query to "top news"
        else:
            get_news(command)  # Otherwise, pass the whole command to get specific news
        return  # Exit early if news info is processed

    # Web search command
    elif any(keyword in command for keyword in SEARCH_KEYWORDS):
        query = command
        for keyword in SEARCH_KEYWORDS:
            query = query.replace(keyword, '').strip()  # Remove the keyword from the command to extract the search query
        if query:
            search_result = search_web(query)
            if search_result:
                talk(search_result)
            else:
                talk(f"Sorry, I couldn't find any results for '{query}'.")
        else:
            talk("Please provide something to search for.")
        return  # Exit early if search is processed

    # Calculation command
    elif any(keyword in command for keyword in CALCULATION_KEYWORDS):
        expression = command.replace('calculate', '').strip()
        result = calculate(expression)
        if result:
            talk(f"{result}")
        else:
            talk(f"Sorry, I couldn't calculate {expression}.")

    # Smart home control command
    elif 'turn on' in command or 'turn off' in command:
        control_device(command)

    # If the command doesn't match any known keywords, pass it to ChatGPT
    else:
        logging.info("Passing the command to ChatGPT because it is not in my commands list...")
        chatgpt_response = get_chatgpt_response(command)
        if chatgpt_response:
            talk(chatgpt_response)
        else:
            talk(f"Sorry, {USER_TITLE}, I am not familiar with that command.")