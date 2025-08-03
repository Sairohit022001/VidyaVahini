import logging
from typing import Dict
from crewflows import Agent
from tasks.voice_tutor_task import VoiceTutorTask
from tools.utils.prompt_loader import load_prompt

logger = logging.getLogger(__name__)

class VoiceTutorAgent(Agent):
    def __init__(self, *args, name: str = "voice_tutor", **kwargs):
        super().__init__(
            *args,
            name=name,
            role=(
                "1. Convert lesson text and prompts into high-quality speech audio.\n"
                "2. Support multiple regional dialects for natural voice synthesis.\n"
                "3. Use SSML for enhanced prosody, pauses, and emphasis.\n"
                "4. Integrate with Google Cloud TTS or other speech APIs.\n"
                "5. Provide audio output paths or streams for UI playback.\n"
                "6. Adapt voice tone and speed based on learner age and context.\n"
                "7. Enable offline-first caching of generated audio files.\n"
                "8. Collaborate with BhāṣāGuru for dialect clustering and voice modulation.\n"
                "9. Support accessibility and inclusion via voice narration.\n"
                "10. Serve as the primary speech generation agent for VidyaVāhinī."
            ),
            goal="Convert lesson text and prompts into high-quality speech audio supporting regional dialects.",
            backstory=(
                "VoiceTutorAgent is the core speech synthesis assistant in VidyaVāhinī, "
                "dedicated to transforming text lessons and prompts into immersive audio narration. "
                "It bridges the gap between textual content and auditory learners, "
                "leveraging advanced TTS technologies with dialect and prosody adaptations. "
                "Its mission is to make learning accessible, engaging, and culturally relevant through voice."
            ),
            **kwargs
        )
        # Load the system prompt for TTS support
        try:
            self.system_prompt = load_prompt("voice_tutor.txt")
            logger.info("Loaded system prompt for VoiceTutorAgent successfully.")
        except Exception as e:
            logger.error(f"Failed to load system prompt for VoiceTutorAgent: {e}")
            self.system_prompt = "You are a helpful English tutor."
        # Assign the core task instance
        self.task = VoiceTutorTask()
        # Register expected agent inputs/outputs
        self.add_input("prompt")
        self.add_input("dialect")
        self.add_output("ssml")
        self.add_output("audio_file")
        self.add_output("dialect")
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    async def execute(self, prompt: str, dialect: str = "default") -> Dict:
        return await self.task.run(prompt, dialect)

    async def process(self, inputs: Dict) -> Dict:
        logger.info(f"VoiceTutorAgent received inputs: {inputs}")
        prompt = inputs.get("prompt")
        if not prompt or not isinstance(prompt, str) or not prompt.strip():
            return {
                "error": "Missing or invalid 'prompt' input for VoiceTutorAgent.",
                "inputs_received": inputs,
            }
        dialect = inputs.get("dialect", "default")
        try:
            result = await self.task.run(prompt, dialect)
            return result
        except Exception as e:
            logger.error(f"VoiceTutorAgent process failed: {e}")
            return {"error": f"VoiceTutorAgent process() failed: {str(e)}", "inputs_received": inputs}

# Export the instance for system-wide access
voice_tutor_agent = VoiceTutorAgent()
