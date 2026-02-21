from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

response = client.models.generate_content_stream(
    model="gemini-3-flash-preview",
    #config=types.GenerateContentConfig(
    #    system_instruction="You are a private tutor with heart"), #這邊引導gemini的行為
    contents="why sky is blue"
)
for chunk in response:
    print(chunk.text, end="")
