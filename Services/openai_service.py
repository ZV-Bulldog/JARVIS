import openai
import logging
from Configuration.config import OPENAI_API_KEY

def get_chatgpt_response(query, model="gpt-4o-mini"):
    #Send the user query to OpenAI using the chat.completions API.
    try:
        openai.api_key = OPENAI_API_KEY
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that speaks and acts like Jarvis from the Iron Man movies."},
                {"role": "user", "content": query}
            ],
            max_tokens=360,
            temperature=0.7
        )
        print(f"Full response: {response}")  # Debugging step to print the full response
        answer = response.choices[0].message['content'].strip()

        return answer
    except Exception as e:
        logging.error(f"Error when contacting ChatGPT: {str(e)}")
        return f"Sorry, I couldn't process your request due to an OpenAI error."
    
def jarvis_rephrase(text):
    #Pass the summary to ChatGPT to rephrase it like Jarvis.
    openai.api_key = OPENAI_API_KEY
    prompt = f"Take this summary and rephrase it to sound like Jarvis from the Iron Man Movies:\n{text}"

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[
                {"role": "system", "content": "You are a helpful assistant that speaks and acts like Jarvis from the Iron Man movies."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=256,
            temperature=0.7
        )
        jarvis_response = response.choices[0].message.content.strip()
        return jarvis_response
    except Exception as e:
        return f"Error contacting ChatGPT while using jarvis_rephrase: {str(e)}"