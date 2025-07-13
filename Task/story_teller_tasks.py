from crewai import Task
from pydantic import BaseModel, Field
from typing import List

# Step 1: Define the structured JSON output format
class StoryOutputSchema(BaseModel):
    title: str = Field(..., description="Creative, catchy title of the story based on the topic")
    story_body: str = Field(..., description="Full narrative story explaining the topic using cultural elements, characters, and situations")
    moral: str = Field(..., description="Clear value/moral takeaway from the story, aligned with educational outcomes")
    suggested_visuals: List[str] = Field(..., description="List of 3–5 scene-level visual prompts to generate illustrations")
    dialect: str = Field(..., description="Name of dialect used for tone adaptation (e.g., Telangana Telugu)")
    story_mode: str = Field(
        default="modern",
        description="Type of storytelling mode: 'modern', 'moral', 'mythological' (Sanātana), or 'folk'"
    )

# Step 2: Define the Task using CrewAI's Task class
generate_story_task = Task(
    name="Generate Contextual Story",
    description=(
        "Create a localized, classroom-appropriate story to teach a selected academic topic. "
        "The story should be engaging, age-appropriate, and culturally rooted using the selected dialect. "
        "Story length should be ~150–300 words, and it should embed a moral aligned with learning. "
        "Add 3–5 visual prompts for scene illustration and BhāṣāGuru audio generation. "
        "Story mode is configurable: "
        "'modern' – School life and day-to-day stories; "
        "'moral' – Everyday situations with life lessons; "
        "'mythological' – Sanātana/epic style with Vedic or Puranic tones; "
        "'folk' – Local legends, tribal myths, or native folklore. "
        "Ensure the output follows StoryOutputSchema, is non-plagiarized, and can be reused by other agents like VisualAgent and VoiceTutorAgent."
    ),
    expected_output=StoryOutputSchema,
    output_json=True,
    context_injection=True
)
