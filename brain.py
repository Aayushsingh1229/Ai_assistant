import requests
import os
from dotenv import dotenv_values

# Load API Key from .env file
env_vars=dotenv_values(".env")
GROQ_API_KEY = env_vars.get("GROQ_API_KEY")

# Function to generate response using Groq
def generate_response(user_query):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mixtral-8x7b-32768",  # Or "mixtral-8x7b-32768" for a more powerful model
        "messages": [{"role": "user", "content": user_query}],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "Error: Unable to process request."

