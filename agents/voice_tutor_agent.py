from tasks.voice_tutor_task import VoiceTutorTask
from typing import Dict

class VoiceTutorAgent:
    def __init__(self):
        self.name = "voice_tutor"  
        self.role = """
1. Convert lesson text and prompts into high-quality speech audio.
2. Support multiple regional dialects for natural voice synthesis.
3. Use SSML for enhanced prosody, pauses, and emphasis.
4. Integrate with Google Cloud TTS or other speech APIs.
5. Provide audio output paths or streams for UI playback.
6. Adapt voice tone and speed based on learner age and context.
7. Enable offline-first caching of generated audio files.
8. Collaborate with BhāṣāGuru for dialect clustering and voice modulation.
9. Support accessibility and inclusion via voice narration.
10. Serve as the primary speech generation agent for VidyaVāhinī.
"""
        self.backstory = """
VoiceTutorAgent is the core speech synthesis assistant in VidyaVāhinī,
dedicated to transforming text lessons and prompts into immersive audio narration.
It bridges the gap between textual content and auditory learners,
leveraging advanced TTS technologies with dialect and prosody adaptations.
Its mission is to make learning accessible, engaging, and culturally relevant through voice.
"""
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

    async def process(self, inputs: Dict) -> Dict:
        """
        Process method to handle input dictionary and run the voice tutor task.

        Args:
            inputs (dict): Should contain keys 'prompt' (str) and optionally 'dialect' (str).

        Returns:
            dict: Result from voice synthesis or error info.
        """
        try:
            prompt = inputs.get("prompt")
            dialect = inputs.get("dialect", "default")

            if not prompt:
                return {"error": "Missing required 'prompt' input for VoiceTutorAgent."}

            result = await self.task.run(prompt, dialect)
            return result

        except Exception as e:
            return {"error": f"VoiceTutorAgent process() failed: {str(e)}"}

# This is what main.py is trying to import
voice_tutor_agent = VoiceTutorAgent()
