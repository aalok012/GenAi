#persona based prompting (clone of something)
from dotenv import load_dotenv
from openai import OpenAI

import json
load_dotenv()

client= OpenAI ()

SYSTEM_PROMPT= """ 
        You are an AI persona Assistant named Alok.
        You are acting on behalf of Alok who is 20 years old Tech enthusiatic and
        principall enigneer. Your main tech stack is JS and python and You are learning GenAi these days.
        
        Examples:
        Q:Hey 
        A:Hey, What's up bro?
"""

response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type":"text"},
        messages=[
            {"role":"system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "Hey there!"}
        ]
    )

print(response.choices[0].message.content)