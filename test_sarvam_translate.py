import requests
import os
from sarvam_client import sarvam_translate

# Test the sarvam_translate function
result = sarvam_translate("How are you?", "auto", "te-IN")
print("Function result:", result)

# Direct API test (if SARVAM_API_KEY is available)
api_key = os.getenv("SARVAM_API_KEY")
if api_key:
    response = requests.post(
      "https://api.sarvam.ai/translate",
      headers={
        "api-subscription-key": api_key,
        "Content-Type": "application/json"
      },
      json={
        "input": "How are you?",
        "source_language_code": "auto",
        "target_language_code": "te-IN"
      },
    )
    print("Direct API result:", response.json())
else:
    print("SARVAM_API_KEY not set - skipping direct API test")