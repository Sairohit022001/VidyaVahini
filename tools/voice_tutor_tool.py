import os
import uuid
from google.cloud import texttospeech

class VoiceTutorTool:
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()
        self.audio_output_dir = "generated_audio"
        os.makedirs(self.audio_output_dir, exist_ok=True)

    def generate_voice_tutor(self, text: str, dialect: str = "default") -> dict:
        # Build SSML with dialect-specific prosody or voice selection here
        ssml = self._build_ssml(text, dialect)

        synthesis_input = texttospeech.SynthesisInput(ssml=ssml)

        voice_params = self._get_voice_params(dialect)
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

        response = self.client.synthesize_speech(
            input=synthesis_input,
            voice=voice_params,
            audio_config=audio_config
        )

        file_name = f"{uuid.uuid4()}.mp3"
        file_path = os.path.join(self.audio_output_dir, file_name)

        with open(file_path, "wb") as out:
            out.write(response.audio_content)

        return {
            "ssml": ssml,
            "audio_file": file_path,
            "dialect": dialect
        }

    def _build_ssml(self, text: str, dialect: str) -> str:
        # Customize SSML here based on dialect
        # Example minimal SSML wrapper:
        return f"<speak>{text}</speak>"

    def _get_voice_params(self, dialect: str) -> texttospeech.VoiceSelectionParams:
        # Map dialect to Google TTS voice names or languages
        voices = {
            "default": texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE),
            "telangana": texttospeech.VoiceSelectionParams(language_code="te-IN", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE),
            "andhra": texttospeech.VoiceSelectionParams(language_code="te-IN", ssml_gender=texttospeech.SsmlVoiceGender.MALE),
        }
        return voices.get(dialect.lower(), voices["default"])
