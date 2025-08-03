import json
import logging
from typing import Dict
from crewflows import Agent

logger = logging.getLogger(__name__)

class StoryTellerAgent(Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            name="story_teller_agent",
            role="Narrative and story-generation agent for topic illustration and engagement.",
            goal="Generate rich, contextual stories from lesson topics with region-specific cultural flavor and visualization prompts.",
            **kwargs
        )
        self._name = "story_teller_agent"
    
    @property
    def name(self) -> str:
        return self._name

    async def process(self, inputs: Dict) -> Dict:
        """
        Generate a culturally contextualized story with visualization prompts and narration.

        Args:
            inputs (Dict): Should contain keys like 'topic', 'dialect', 'prompt', etc.

        Returns:
            Dict: JSON-compatible dictionary with story content and metadata.
        """
        topic = inputs.get("topic", "General")
        dialect = inputs.get("dialect", "default")
        prompt = inputs.get("prompt", "")

        logger.info(f"StoryTellerAgent processing topic: {topic}, dialect: {dialect}")

        try:
            # Placeholder static story — replace with actual calls to LLM or generation logic
            generated_story_json = """
            {
                "story_title": "The Magical Tale of Photosynthesis",
                "story_body": "Once upon a time in a Telangana village, a little plant learned how to make food using sunlight...",
                "moral": "Respect and protect nature.",
                "visual_prompts": ["Sunlight shining on green leaves", "Village landscape with a plant"],
                "localized_dialect_story": "Telangana dialect version of the story goes here.",
                "audio_narration": ""
            }
            """
            story_data = json.loads(generated_story_json)

            required_keys = {
                "story_title",
                "story_body",
                "moral",
                "visual_prompts",
                "localized_dialect_story",
                "audio_narration"
            }
            missing_keys = required_keys - story_data.keys()
            if missing_keys:
                raise ValueError(f"Missing keys in story output: {missing_keys}")

            return story_data

        except Exception as e:
            logger.error(f"Error generating story: {e}", exc_info=True)
            return {
                "story_title": "Error generating story",
                "story_body": f"An error occurred: {str(e)}",
                "moral": "",
                "visual_prompts": [],
                "localized_dialect_story": "",
                "audio_narration": ""
            }


# Instantiate the single StoryTellerAgent for use
story_teller_agent = StoryTellerAgent()
