import os
import base64
from tempfile import NamedTemporaryFile
from google.cloud import texttospeech

# Minimal BaseTool definition to replace missing import
class BaseTool:
    def __init__(self):
        pass

# Dialect prosody settings
DIALECT_PROSODY = {
    "andhra": {
        "rate": "medium",
        "pitch": "+2st"
    },
    "telangana": {
        "rate": "slow",
        "pitch": "-2st"
    },
    "neutral": {
        "rate": "medium",
        "pitch": "0st"
    }
}

class VoiceTutorTool(BaseTool):
    name = "Voice Tutor Tool"
    description = "Converts text/lesson content into region-specific voice with SSML prosody"
    
    def __init__(self):
        super().__init__()
        # Initialize GCP TTS client
        self.client = texttospeech.TextToSpeechClient()

    def _get_prosody_settings(self, dialect: str):
        return DIALECT_PROSODY.get(dialect.lower(), DIALECT_PROSODY["neutral"])

    def _wrap_ssml(self, text: str, dialect: str):
        prosody = self._get_prosody_settings(dialect)
        return f"""
            <speak>
                <prosody rate="{prosody['rate']}" pitch="{prosody['pitch']}">
                    {text}
                </prosody>
            </speak>
        """

    def _synthesize_speech(self, ssml: str):
        synthesis_input = texttospeech.SynthesisInput(ssml=ssml)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-IN",
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = self.client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        return response.audio_content

    def run(self, prompt: str, dialect: str = "neutral"):
        try:
            # Wrap prompt with SSML for prosody
            ssml_text = self._wrap_ssml(prompt, dialect)

            # Synthesize speech audio content
            audio_content = self._synthesize_speech(ssml_text)

            # Save audio temporarily to a file
            with NamedTemporaryFile(delete=False, suffix=".mp3") as out:
                out.write(audio_content)
                out.flush()
                audio_path = out.name

            # Read audio and encode to base64 for transmission
            with open(audio_path, "rb") as audio_file:
                base64_audio = base64.b64encode(audio_file.read()).decode("utf-8")

            # Clean up temporary audio file
            os.remove(audio_path)

            return {
                "audio_base64": base64_audio,
                "dialect": dialect,
                "ssml_used": ssml_text.strip()
            }

        except Exception as e:
            return {
                "error": str(e),
                "dialect": dialect,
                "ssml_attempted": ssml_text if 'ssml_text' in locals() else None
            }
