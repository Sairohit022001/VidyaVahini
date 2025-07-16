from crewflows import Task
from pydantic import BaseModel, Field
from typing import List

class StoryOutputSchema(BaseModel):
    title: str = Field(..., description="Engaging title of the story")
    story_body: str = Field(..., description="Full story in 150–300 words using cultural relevance")
    moral: str = Field(..., description="Educational takeaway from the story")
    suggested_visuals: List[str] = Field(..., description="Scene-level prompts for visual generation")
    dialect: str = Field(..., description="Dialect used (e.g., Telangana Telugu)")

generate_story_task = Task(
    name="Generate Contextual Academic Story",
    description=(
        "Receive topic, grade level, and dialect.\n"
        "Create a story that illustrates the topic with relatable characters.\n"
        "Adapt tone based on student age (funny for kids, abstract for older students).\n"
        "Include a short moral linked to the lesson theme.\n"
        "Add suggested visuals for VisualAgent.\n"
        "Maintain cultural grounding and classroom appropriateness.\n"
        "Avoid plagiarism and AI hallucination.\n"
        "Embed emotion, curiosity, and humor for engagement.\n"
        "Return JSON as per StoryOutputSchema.\n"
        "Use dialect requested for BhāṣāGuru narration compatibility."
    ),
    expected_output=StoryOutputSchema,
    output_json=True,
    context_injection=True,
    verbose=True,
    output_file="outputs/story_output_{timestamp}.json",
    guardrails={
        "retry_on_fail": 1,
        "fallback_response": {
            "title": "Default Story Title",
            "story_body": "No story generated.",
            "moral": "Learning is fun!",
            "suggested_visuals": [],
            "dialect": "Telangana Telugu"
        }
    },
    metadata={
        "agent": "StoryTellerAgent",
        "access": "teacher_only",
        "downstream": ["VisualAgent", "BhāṣāGuru"],
        "triggers": ["on_story_request"]
    }
)

