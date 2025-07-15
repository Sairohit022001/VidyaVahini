from tools.voice_tutor_tool import VoiceTutorTool

class VoiceTutorTask:
    def __init__(self):
        self.tool = VoiceTutorTool()

    def run(self, input_text: str, dialect: str = "default") -> dict:
        """
        Run the Voice Tutor task: generate SSML and audio file for given text and dialect.

        Args:
            input_text (str): The text to synthesize.
            dialect (str): Dialect to use ('telangana', 'andhra', or 'default').

        Returns:
            dict: {
                "ssml": SSML string,
                "audio_file": path to generated audio file,
                "dialect": dialect used
            }
        """
        result = self.tool.generate_voice_tutor(input_text, dialect)
        return result
