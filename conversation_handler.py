import json
import os
from datetime import datetime, timedelta
import openai
from Configuration.config import OPENAI_API_KEY

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

CONVERSATION_FILE = "data/conversations.json"

def save_conversation(user_query, assistant_response):
    conversation = {
        "user_query": user_query,
        "assistant_response": assistant_response,
        "timestamp": datetime.now().isoformat()
    }
    
    # Check if the file exists and is not empty
    if os.path.exists(CONVERSATION_FILE) and os.path.getsize(CONVERSATION_FILE) > 0:
        with open(CONVERSATION_FILE, "r") as file:
            try:
                conversations = json.load(file)
            except json.JSONDecodeError:
                # If there's an error decoding, reset the conversations list
                conversations = []
    else:
        conversations = []

    # Append the new conversation
    conversations.append(conversation)
    
    # Save updated conversations
    with open(CONVERSATION_FILE, "w") as file:
        json.dump(conversations, file, indent=4)

# Function to summarize old conversations using GPT-3
def summarize_conversation(conversation):
    summary_prompt = f"Summarize the following conversation:\nUser: {conversation['user_query']}\nAssistant: {conversation['assistant_response']}"
    
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant. Summarize conversations."},
                {"role": "user", "content": summary_prompt}
            ],
            max_tokens=256,
            temperature=0.5
        )
        summary = response['choices'][0]['message']['content'].strip()
        return summary
    except Exception as e:
        print(f"Error summarizing conversation: {str(e)}")
        return None

# Function to chunk and summarize old conversations
def chunk_and_summarize_conversations():
    if os.path.exists(CONVERSATION_FILE):
        with open(CONVERSATION_FILE, "r") as file:
            conversations = json.load(file)
        
        current_time = datetime.now()

        # Split into recent (within a week) and older (between 1 week and 1 month)
        recent_conversations = [conv for conv in conversations if datetime.fromisoformat(conv["timestamp"]) > current_time - timedelta(weeks=1)]
        older_conversations = [conv for conv in conversations if current_time - timedelta(weeks=4) < datetime.fromisoformat(conv["timestamp"]) <= current_time - timedelta(weeks=1)]
        
        # Create summarized version for older conversations
        summarized_conversations = []
        for conv in older_conversations:
            summary = summarize_conversation(conv)
            if summary:
                summarized_conversations.append({
                    "summary": summary,
                    "timestamp": conv["timestamp"]
                })
        
        # Combine recent and summarized conversations
        all_conversations = recent_conversations + summarized_conversations

        # Save updated conversation data
        with open(CONVERSATION_FILE, "w") as file:
            json.dump(all_conversations, file, indent=4)

# Function to clear conversations (for when leaving beta phase)
def clear_training_data():
    if os.path.exists(CONVERSATION_FILE):
        os.remove(CONVERSATION_FILE)

# Function to load recent conversations for memory (last 7 days)
def load_recent_conversations():
    if os.path.exists(CONVERSATION_FILE):
        with open(CONVERSATION_FILE, "r") as file:
            conversations = json.load(file)
        
        current_time = datetime.now()
        recent_conversations = [conv for conv in conversations if datetime.fromisoformat(conv["timestamp"]) > current_time - timedelta(weeks=1)]
        
        return recent_conversations
    else:
        return []

# Call this function periodically to summarize older conversations
def periodic_chunking():
    chunk_and_summarize_conversations()