from serpapi import GoogleSearch
from Configuration.config import SERPAPI_API_KEY, DEFAULT_LOCATION, OPENAI_API_KEY
from Configuration.voice_interaction import talk
from Services.openai_service import get_chatgpt_response, jarvis_rephrase
import openai

openai.api_key = OPENAI_API_KEY

# Example update for weather service
def get_weather():
    print("Running the get_weather function")
    params = {"q": f"weather {DEFAULT_LOCATION}", "api_key": SERPAPI_API_KEY}
    search = GoogleSearch(params)
    results = search.get_dict()

    if "organic_results" in results and results['organic_results']:
        weather_info = results['organic_results'][0]['snippet']
        print(f"Weather: {weather_info}")
        jarvis_response = jarvis_rephrase(f"The current weather is: {weather_info}")
        talk(jarvis_response)
    else:
        weather_info = "Weather information not available."
        talk(jarvis_rephrase(weather_info))

def get_news(command):
    print("Running the get_news function")
    
    # Define parameters for the SerpAPI Google News search
    params = {
        "engine": "google_news",  # Specify the engine
        "q": command,          # Query for the top news
        "gl": "us",               # Country (US in this case)
        "hl": "en",               # Language (English in this case)
        "api_key": SERPAPI_API_KEY # Your API key
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()

    if "news_results" in results:
        news_results = results["news_results"]
        news_summary = "Here are the top news headlines:\n"
        
        # Loop through the top 5 results to generate a summary
        for result in news_results[:5]:
            title = result.get('title', 'No title')
            link = result.get('link', 'No link')
            source_name = result.get('source', {}).get('name', 'Unknown source')
            snippet = result.get('snippet', 'No snippet available')
            
            # Build a news summary string
            news_summary += f"Title: {title}\nSource: {source_name}\nSnippet: {snippet}\nLink: {link}\n\n"
        
        # Rephrase the news summary like Jarvis
        jarvis_response = jarvis_rephrase(news_summary.strip())
        talk(jarvis_response)  # Speak the response

    else:
        print("No news results found.")
        talk(jarvis_rephrase("Sorry, I couldn't retrieve the news."))

def search_web(query):
    print(f"Searching the web for: {query}")
    """Search the web, generate a summary, and pass it to ChatGPT for rephrasing like Jarvis."""
    params = {
        "q": query,
        "api_key": SERPAPI_API_KEY
    }
    search = GoogleSearch(params)
    results = search.get_dict()

    # Check if "ai_overview" is available in the results to prevent KeyError
    if "ai_overview" in results:
        ai_overview = results['ai_overview']
        summary = "Here are the search highlights:\n"
        
        # Extract paragraphs and lists
        for block in ai_overview.get('text_blocks', []):
            if block['type'] == 'paragraph':
                summary += f"{block['snippet']}\n"
            elif block['type'] == 'list':
                for item in block['list']:
                    summary += f"- {item['snippet']}\n"

        # Pass the summary to ChatGPT to rephrase like Jarvis
        jarvis_response = jarvis_rephrase(summary)
        return jarvis_response

    else:
        # No AI overview available, pass the original query to ChatGPT
        no_overview_message = f"There is no AI overview for '{query}' on the web, Sir. I will try again a different way."
        talk(no_overview_message)
        print(no_overview_message)

        # Pass the original query to ChatGPT to generate a response
        chatgpt_response = get_chatgpt_response(query)
        return chatgpt_response
