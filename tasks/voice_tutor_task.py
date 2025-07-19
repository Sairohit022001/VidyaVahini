from typing import Dict
from tools.voice_tutor_tool import VoiceTutorTool

class VoiceTutorTask:
    def __init__(self):
        self.tool = VoiceTutorTool()

    async def run(self, input_text: str, dialect: str = "default") -> Dict[str, str]:
        """
        Generate SSML and audio file for given text and dialect using the VoiceTutorTool.

        Args:
            input_text (str): Text content to synthesize into speech.
            dialect (str): Dialect to use ('telangana', 'andhra', or 'default').

        Returns:
            dict: {
                "ssml": str,         # Generated SSML markup
                "audio_file": str,   # Path or URL to the generated audio file
                "dialect": str       # Dialect used in synthesis
            }
        Raises:
            RuntimeError: If voice generation fails.
        """
        try:
            # Assuming generate_voice_tutor is synchronous, no await here
            result = self.tool.generate_voice_tutor(input_text, dialect)
            return result
        except Exception as e:
            raise RuntimeError(f"VoiceTutorTask failed: {str(e)}") from e
