# tools/voice_tutor_tool.py

"""
Voice Tutor Tool

This module handles:
- Dialect-based clustering for Telugu regions
- SSML generation with prosody tuning
- Google Cloud Text-to-Speech API integration
- Audio synthesis and base64 output for UI compatibility

Usage:
    voice_tool = VoiceTutorTool()
    audio_data = voice_tool.run(text="Photosynthesis is...", dialect="Telangana Telugu", student_level="beginner")
"""

import os
import base64
from typing import Literal, Dict
from google.cloud import texttospeech
from dotenv import load_dotenv

load_dotenv()

class VoiceTutorTool:
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()
        self.voice_mapping = {
            "Telangana": "te-IN-Wavenet-A",
            "Andhra": "te-IN-Wavenet-B",
            "Rayalaseema": "te-IN-Wavenet-C"
        }
        self.default_voice = "te-IN-Wavenet-A"
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

    def _detect_dialect_cluster(self, dialect: str) -> str:
        """Map user dialect to one of the known clusters."""
        if "telangana" in dialect.lower():
            return "Telangana"
        elif "andhra" in dialect.lower():
            return "Andhra"
        elif "rayalaseema" in dialect.lower():
            return "Rayalaseema"
        else:
            return "Telangana"  # Fallback default

    def _generate_ssml(self, text: str, level: Literal["beginner", "intermediate", "advanced"]) -> str:
        """Return SSML markup with prosody settings."""
        prosody_settings = {
            "beginner": {"rate": "slow", "pitch": "+2st"},
            "intermediate": {"rate": "medium", "pitch": "+1st"},
            "advanced": {"rate": "fast", "pitch": "0st"}
        }
        settings = prosody_settings.get(level, prosody_settings["beginner"])
        ssml = f"""
        <speak>
          <prosody rate="{settings['rate']}" pitch="{settings['pitch']}">
            {text}
          </prosody>
        </speak>
        """
        return ssml.strip()

    def _synthesize_speech(self, ssml: str, voice_name: str) -> bytes:
        """Call GCP API and return synthesized audio bytes."""
        input_text = texttospeech.SynthesisInput(ssml=ssml)
        voice_params = texttospeech.VoiceSelectionParams(
            language_code="te-IN",
            name=voice_name
        )
        response = self.client.synthesize_speech(
            input=input_text,
            voice=voice_params,
            audio_config=self.audio_config
        )
        return response.audio_content

    def run(self, text: str, dialect: str, student_level: str = "beginner") -> Dict:
        """
        Main entry point to generate voice output.

        Parameters:
        - text (str): The explanation or story content
        - dialect (str): User's regional dialect ("Telangana Telugu")
        - student_level (str): Reading level - beginner, intermediate, advanced

        Returns:
        - dict: {
            "audio_base64": <base64 string>,
            "ssml_used": <ssml string>,
            "voice_model": <voice name>
        }
        """
        try:
            cluster = self._detect_dialect_cluster(dialect)
            voice_name = self.voice_mapping.get(cluster, self.default_voice)
            ssml = self._generate_ssml(text, student_level)
            audio_bytes = self._synthesize_speech(ssml, voice_name)
            audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

            return {
                "audio_base64": audio_base64,
                "ssml_used": ssml,
                "voice_model": voice_name
            }
        except Exception as e:
            return {
                "error": str(e),
                "audio_base64": None,
                "ssml_used": "",
                "voice_model": "undefined"
            }

# ✅ Singleton instance
voice_tutor_tool = VoiceTutorTool()
