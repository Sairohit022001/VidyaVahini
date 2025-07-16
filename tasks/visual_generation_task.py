from crewflows import Task
from pydantic import BaseModel, Field
from typing import List

class VisualOutputSchema(BaseModel):
    topic: str = Field(..., description="Topic name or concept title")
    visual_prompts: List[str] = Field(..., description="List of DALL-E/Gemini prompts for generating visual scenes")
    grade_level: str = Field(..., description="Class/Grade level to adapt visual style")
    dialect_style: str = Field(..., description="Tone/dialect for cultural style (e.g., Telangana Telugu)")
    image_styles: List[str] = Field(..., description="Style hints like cartoon, diagram, sketch")

generate_visual_task = Task(
    name="Generate Visual Concepts",
    description=(
        "Accept summary, story, or keywords for the topic.\n"
        "Convert them into 3–5 high-quality visual prompts.\n"
        "Choose image styles based on grade (cartoon, diagram, etc).\n"
        "Ensure tone, symbols, and visuals are culturally grounded.\n"
        "Support dialectal and regional context in design.\n"
        "Outputs usable by Gemini Vision or DALL-E.\n"
        "Return JSON following VisualOutputSchema.\n"
        "Work in tandem with StoryTellerAgent or QuizAgent.\n"
        "Avoid offensive or biased imagery.\n"
        "Include hints for audio-visual narration if needed."
    ),
    expected_output=VisualOutputSchema,
    output_json=True,
    context_injection=True,
    verbose=True,
    output_file="outputs/visual_output_{timestamp}.json",
    guardrails={
        "retry_on_fail": 2,
        "fallback_response": {
            "topic": "Unknown",
            "visual_prompts": [],
            "grade_level": "Unknown",
            "dialect_style": "Telangana Telugu",
            "image_styles": ["cartoon"]
        }
    },
    metadata={
        "agent": "VisualAgent",
        "access": "teacher_and_student_above_grade_10",
        "downstream": ["BhāṣāGuru"],
        "triggers": ["on_story_completion", "on_teacher_request"]
    }
)
