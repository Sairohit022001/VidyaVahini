import requests
import os

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

def sarvam_translate(text: str, source_lang: str, target_lang: str):
    url = "https://api.sarvam.ai/translate"  
    headers = {
        "Authorization": f"Bearer {SARVAM_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "source_lang": source_lang, 
        "target_lang": target_lang    
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()
