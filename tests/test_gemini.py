from google import genai

client = genai.Client(api_key="AIzaSyAiH_DE8oNT9UqLqt9foPzlXMo3DXP-BD0")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain artificial intelligence in one sentence"
)

print(response.text)  










