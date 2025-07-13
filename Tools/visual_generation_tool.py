import os
from typing import Dict, List
from langchain_core.tools import Tool
import random

from dotenv import load_dotenv
load_dotenv()

class VisualGenerationTool:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.visual_provider = "dalle"  

    def _dalle_prompt_generator(self, topic: str, dialect: str, age_group: str) -> List[str]:
        """
        Generate 3–5 scene-level prompts contextualized for Indian classrooms.
        """
        prompt_templates = [
            f"A colorful cartoon showing '{topic}' in a rural Indian school, explained in {dialect}",
            f"An infographic of '{topic}' for age group {age_group} using simple visual icons",
            f"A realistic diagram showing the concept of '{topic}' for children in a Telugu-speaking village",
            f"Classroom blackboard-style image illustrating '{topic}' for Grade {age_group}",
            f"A comic-strip style image showing how '{topic}' happens in real life"
        ]
        return random.sample(prompt_templates, 3)

    def run(self, inputs: Dict) -> Dict:
        """
        Expected inputs:
            {
                "topic": "Photosynthesis",
                "age_group": "6-10 years",
                "dialect": "Telangana Telugu",
                "visual_type": "cartoon"  # or 'diagram', 'infographic'
            }
        """
        topic = inputs.get("topic", "Photosynthesis")
        age_group = inputs.get("age_group", "6–10 years")
        dialect = inputs.get("dialect", "Telangana Telugu")
        visual_type = inputs.get("visual_type", "cartoon")

        # Generate prompts
        prompts = self._dalle_prompt_generator(topic, dialect, age_group)

        # Simulate image generation URLs (replace with actual OpenAI API later)
        image_urls = [f"https://dummyimage.com/600x400/000/fff&text={topic.replace(' ', '+')}+{i+1}" for i in range(len(prompts))]

        return {
            "topic_title": topic,
            "scene_prompts": prompts,
            "visual_type": visual_type,
            "age_group": age_group,
            "dialect_context": dialect,
            "image_urls": image_urls
        }