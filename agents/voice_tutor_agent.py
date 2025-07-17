from tasks.voice_tutor_task import VoiceTutorTask
from typing import Dict

class VoiceTutorAgent:
    def __init__(self):
        self.name = "voice_tutor"  # ✅ Added this line
        self.task = VoiceTutorTask()

    async def execute(self, prompt: str, dialect: str = "default") -> Dict:
        """
        Execute the Voice Tutor agent asynchronously.

        Args:
            prompt (str): Text prompt to convert to speech.
            dialect (str): Dialect for voice synthesis.

        Returns:
            dict: Output from the VoiceTutorTask with SSML, audio path, and dialect info.
        """
        return await self.task.run(prompt, dialect)

# This is what main.py is trying to import
voice_tutor_agent = VoiceTutorAgent()
