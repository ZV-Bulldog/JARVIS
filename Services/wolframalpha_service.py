import wolframalpha
from Configuration.config import WOLFRAMALPHA_APP_ID
import openai

def calculate(expression):
    print("Running the calculate function")
    client = wolframalpha.Client(WOLFRAMALPHA_APP_ID)
    res = client.query(expression)
    result = next(res.results).text
    jarvis_response = (f"The result is {result}")
    return jarvis_response