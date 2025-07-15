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
        # Could add input validation or dialect detection here if needed
        return self.task.run(prompt, dialect)
