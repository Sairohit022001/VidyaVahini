from langchain_google_genai import ChatGoogleGenerativeAI

llm_25 = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-pro",
    google_api_key="YOUR_API_KEY",
    temperature=0.3
)

try:
    response = llm_25.invoke([{"role": "user", "content": "Hello, test Gemini 2.5!"}])
    print("2.5-pro model works:", response)
except Exception as e:
    print("2.5-pro error:", e)

llm_15 = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-pro",
    google_api_key="YOUR_API_KEY",
    temperature=0.3
)

try:
    response = llm_15.invoke([{"role": "user", "content": "Hello, test Gemini 1.5!"}])
    print("1.5-pro model works:", response)
except Exception as e:
    print("1.5-pro error:", e)
