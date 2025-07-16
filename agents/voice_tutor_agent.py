from tasks.voice_tutor_task import VoiceTutorTask

class VoiceTutorAgent:
    def __init__(self):
        self.task = VoiceTutorTask()

    def execute(self, prompt: str, dialect: str = "default") -> dict:
        """
        Execute the Voice Tutor agent.

        Args:
            prompt (str): Text prompt to convert to speech.
            dialect (str): Dialect for voice synthesis.

        Returns:
            dict: Output from the VoiceTutorTask with SSML, audio path, and dialect info.
        """
        return self.task.run(prompt, dialect)

# ✅ This is what main.py is trying to import
voice_tutor_agent = VoiceTutorAgent()
