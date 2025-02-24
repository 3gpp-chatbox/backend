# gemini API key test
import requests
import json
from config import Gemini_API_KEY


API_KEY = Gemini_API_KEY
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

headers = {"Content-Type": "application/json"}

data = {"contents": [{"parts": [{"text": "Explain how AI works"}]}]}

response = requests.post(url, headers=headers, json=data)
print(response.json())

# openai API key test
# from openai import OpenAI
# from config import OPENAI_API_KEY

# client = OpenAI(
#   api_key=OPENAI_API_KEY
# )

# completion = client.chat.completions.create(
#   model="gpt-4o-mini",
#   store=True,
#   messages=[
#     {"role": "user", "content": "write a haiku about ai"}
#   ]
# )

# print(completion.choices[0].message);

