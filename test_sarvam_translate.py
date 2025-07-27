import requests

# Translate Text (POST /translate)
response = requests.post(
  "https://api.sarvam.ai/translate",
  headers={
    "api-subscription-key": ""
  },
  json={
    "input": "How are you?",
    "source_language_code": "auto",
    "target_language_code": "te-IN"
  },
)

print(response.json())