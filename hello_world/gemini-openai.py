from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client= OpenAI (
    api_key="AIzaSyBscKnpkaBJmIoZeWNiN6hoV0IFNdNspkw",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response= client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
          { "role": "user", "content": "hey there, do you know my name?"}
        ]
)

print(response.choices[0].message.content)

