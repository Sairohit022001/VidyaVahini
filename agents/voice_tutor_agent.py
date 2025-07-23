from tasks.voice_tutor_task import VoiceTutorTask
from tools.utils.prompt_loader import load_prompt
from typing import Dict
from crewflows import Agent # Import Agent base class
import logging # Import logging
import os
logger = logging.getLogger(__name__) # Get logger for the agent

class VoiceTutorAgent(Agent): # Inherit from Agent for consistency
    def __init__(self):
        super().__init__( # Call super().__init__
            name="voice_tutor",
            role="""1. Convert lesson text and prompts into high-quality speech audio.
                    2. Support multiple regional dialects for natural voice synthesis.
                    3. Use SSML for enhanced prosody, pauses, and emphasis.
                    4. Integrate with Google Cloud TTS or other speech APIs.
                    5. Provide audio output paths or streams for UI playback.
                    6. Adapt voice tone and speed based on learner age and context.
                    7. Enable offline-first caching of generated audio files.
                    8. Collaborate with BhāṣāGuru for dialect clustering and voice modulation.
                    9. Support accessibility and inclusion via voice narration.
                    10. Serve as the primary speech generation agent for VidyaVāhinī.""",
            goal="Convert lesson text and prompts into high-quality speech audio supporting regional dialects.", # Add a goal
            backstory="""VoiceTutorAgent is the core speech synthesis assistant in VidyaVāhinī,
                        dedicated to transforming text lessons and prompts into immersive audio narration.
                        It bridges the gap between textual content and auditory learners,
                        leveraging advanced TTS technologies with dialect and prosody adaptations.
                        Its mission is to make learning accessible, engaging, and culturally relevant through voice.
                        """
        )
        try:
            self.system_prompt = load_prompt("voice_tutor.txt")
            logger.info(f"Loaded system prompt for VoiceTutorAgent successfully.")
        except Exception as e:
            logger.error(f"Failed to load system prompt for VoiceTutorAgent: {e}")
            self.system_prompt = "You are a helpful English tutor."
        self.task = VoiceTutorTask()

    async def execute(self, prompt: str, dialect: str = "default") -> Dict: # async again
        """
        Execute the Voice Tutor agent asynchronously.

        Args:
            prompt (str): Text prompt to convert to speech.
            dialect (str): Dialect for voice synthesis.

        Returns:
            dict: Output from the VoiceTutorTask with SSML, audio path, and dialect info.
        """
        return await self.task.run(prompt, dialect) # await the async task run

    async def process(self, inputs: Dict) -> Dict: # async again
        """
        Process method to handle input dictionary and run the voice tutor task.

        Args:
            inputs (dict): Should contain keys 'prompt' (str) and optionally 'dialect' (str).

        Returns:
            dict: Result from voice synthesis or error info.
        """
        try:
            logger.info(f"VoiceTutorAgent received inputs: {inputs}") # Log inputs
            # Try direct key access with error handling
            try:
                prompt = inputs["prompt"]
            except KeyError:
                return {"error": "Missing required 'prompt' input for VoiceTutorAgent.", "details": "KeyError: 'prompt' not found in inputs.", "inputs_received": inputs}

            logger.info(f"VoiceTutorAgent prompt value (after direct access): {prompt}, type: {type(prompt)}") # Log value and type again

            dialect = inputs.get("dialect", "default")

            # More robust prompt check
            if prompt is None or not isinstance(prompt, str) or not prompt.strip():
                 return {"error": "Missing required 'prompt' input for VoiceTutorAgent.", "details": f"Prompt is not a valid non-empty string. Value: {prompt}, Type: {type(prompt)}", "inputs_received": inputs}


            # Await the async run method of the task
            result = await self.task.run(prompt, dialect)
            return result

        except Exception as e:
            return {"error": f"VoiceTutorAgent process() failed: {str(e)}", "inputs_received": inputs}

# Export instance for import in main.py
voice_tutor_agent = VoiceTutorAgent()

# Add inputs and outputs as in other agents for consistency
voice_tutor_agent.add_input("prompt")
voice_tutor_agent.add_input("dialect")
voice_tutor_agent.add_output("ssml")
voice_tutor_agent.add_output("audio_file")
voice_tutor_agent.add_output("dialect")
