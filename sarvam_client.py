import requests
import os

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

def sarvam_translate(text: str, source_lang: str, target_lang: str):
    if not SARVAM_API_KEY:
        return {"error": "SARVAM_API_KEY not configured"}
    
    url = "https://api.sarvam.ai/translate"  
    headers = {
        "api-subscription-key": SARVAM_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "input": text,
        "source_language_code": source_lang, 
        "target_language_code": target_lang    
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Translation request failed: {str(e)}"}
