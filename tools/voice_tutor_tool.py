import os
import json
from google.cloud import texttospeech

# Set the env var if not already set
GOOGLE_CLOUD_TTS_CREDENTIALS = os.getenv(
    "GOOGLE_APPLICATION_CREDENTIALS",
    "/workspaces/VidyaVahini/VidyaVahini/keys/vidyavahini-tts-f8942d53e066.json"
)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_CLOUD_TTS_CREDENTIALS

# Dialect clustering map example
DIALECT_MAP = {
    "telangana": {
        "language_code": "te-IN",
        "voice_name": "te-IN-Standard-A",  # MALE
        "ssml_gender": texttospeech.SsmlVoiceGender.MALE,
        "prosody_rate": "medium",
        "prosody_pitch": "+0st",
    },
    "andhra": {
        "language_code": "te-IN",
        "voice_name": "te-IN-Standard-B",  # FEMALE
        "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE,
        "prosody_rate": "medium",
        "prosody_pitch": "+1st",
    },
    "default": {
        "language_code": "en-IN",
        "voice_name": "en-IN-Wavenet-D",  # ✅ This still works
        "ssml_gender": texttospeech.SsmlVoiceGender.NEUTRAL,
        "prosody_rate": "medium",
        "prosody_pitch": "+0st",
    },
}


class VoiceTutorTool:
    def __init__(self):
        # No need to reset env var here again, it's already set above
        self.client = texttospeech.TextToSpeechClient()

    def _get_dialect_settings(self, dialect_name: str):
        key = dialect_name.lower()
        return DIALECT_MAP.get(key, DIALECT_MAP["default"])

    def _build_ssml(self, text: str, rate: str, pitch: str):
        ssml_text = f"""
        <speak>
          <prosody rate="{rate}" pitch="{pitch}">
            {text}
          </prosody>
        </speak>
        """
        return ssml_text

    def synthesize_speech(self, text: str, dialect: str = "default", output_path: str = "output.mp3") -> str:
        dialect_settings = self._get_dialect_settings(dialect)

        ssml = self._build_ssml(text, dialect_settings["prosody_rate"], dialect_settings["prosody_pitch"])

        input_text = texttospeech.SynthesisInput(ssml=ssml)

        voice = texttospeech.VoiceSelectionParams(
            language_code=dialect_settings["language_code"],
            name=dialect_settings["voice_name"],
            ssml_gender=dialect_settings["ssml_gender"],
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
        )

        response = self.client.synthesize_speech(
            input=input_text,
            voice=voice,
            audio_config=audio_config,
        )

        with open(output_path, "wb") as out:
            out.write(response.audio_content)

        return output_path

    def generate_voice_tutor(self, text: str, dialect: str = "default") -> dict:
        dialect_settings = self._get_dialect_settings(dialect)
        ssml_text = self._build_ssml(text, dialect_settings["prosody_rate"], dialect_settings["prosody_pitch"])
        output_file = f"voice_tutor_output_{dialect}.mp3"

        audio_path = self.synthesize_speech(text, dialect, output_file)

        return {
            "ssml": ssml_text.strip(),
            "audio_file": audio_path,
            "dialect": dialect,
        }
