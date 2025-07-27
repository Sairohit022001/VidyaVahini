import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def run_story_teller_agent(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a story based on inputs.
    
    Args:
        inputs (Dict[str, Any]): Input parameters, typically including topic, dialect, etc.
    
    Returns:
        Dict[str, Any]: Story data with keys:
            - story_title
            - story_body
            - moral
            - visual_prompts
            - localized_dialect_story
            - audio_narration
    """
    try:
        # Extract key info from inputs
        topic = inputs.get("topic", "Default Topic")
        dialect = inputs.get("dialect", "Generic")
        prompt = inputs.get("prompt", "")

        # Here you would integrate with your LLM or generation logic.
        # For example, send `prompt` to a language model and parse output.

        # Simulated generation of story JSON string (replace with actual API call)
        generated_story_json = """
        {
            "story_title": "The Magical Tale of Photosynthesis",
            "story_body": "Once upon a time in a Telangana village, a little plant learned to make food from sunlight...",
            "moral": "Nature provides for all if we understand and protect it.",
            "visual_prompts": ["Green leaves glowing in sunlight", "Village plant with sun rays"],
            "localized_dialect_story": "Telangana dialect version of the story goes here.",
            "audio_narration": ""
        }
        """

        # Parse the generated JSON string safely
        story_data = json.loads(generated_story_json)

        # Validate expected keys
        required_keys = {
            "story_title", "story_body", "moral",
            "visual_prompts", "localized_dialect_story", "audio_narration"
        }
        missing_keys = required_keys - story_data.keys()
        if missing_keys:
            raise ValueError(f"Missing keys in story output: {missing_keys}")

        return story_data

    except Exception as e:
        logger.error(f"Error in run_story_teller_agent: {e}", exc_info=True)
        # Fallback response
        return {
            "story_title": "Error generating story",
            "story_body": f"An error occurred: {str(e)}",
            "moral": "Keep trying!",
            "visual_prompts": [],
            "localized_dialect_story": f"An error occurred: {str(e)}",
            "audio_narration": ""
        }
