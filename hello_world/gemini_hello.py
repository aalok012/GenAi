from google import genai

client = genai.Client(
     api_key="AIzaSyBscKnpkaBJmIoZeWNiN6hoV0IFNdNspkw"
 )
 

response = client.models.generate_content(
     model="gemini-2.5-flash", contents="explain me water"
 )
print(response.text)