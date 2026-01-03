from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client= OpenAI()

response= client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
          { "role": "user", "content": "hey there, do you know my name?"}
        ]
)

print(response.choices[0].message.content)

