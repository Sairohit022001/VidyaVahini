from crewai import Task
from pydantic import BaseModel, Field
from typing import List

# Step 1: Define the structured output schema
class VisualOutputSchema(BaseModel):
    topic_title: str = Field(..., description="Title of the academic topic")
    scene_prompts: List[str] = Field(..., description="List of 3–5 creative prompts to generate visuals")
    visual_type: str = Field(..., description="Type of visual (e.g., cartoon, infographic, diagram)")
    age_group: str = Field(..., description="Target age group (e.g., 6-10 years, 11-14 years, above 15)")
    dialect_context: str = Field(..., description="Dialect and cultural context used for visual adaptation")
    image_urls: List[str] = Field(default=[], description="Optional list of generated image URLs or placeholders")

# Step 2: Define the agent's core task
generate_visual_task = Task(
    name="Generate Conceptual Visuals",
    description=(
        "1. Receive a topic and grade-level information from upstream agents.\n"
        "2. Analyze the core concept to break it into 3–5 visual scenes.\n"
        "3. Choose the visual style based on age and cultural context.\n"
        "4. Use visual storytelling principles to enhance memory retention.\n"
        "5. Create prompts compatible with DALL·E and Gemini Vision APIs.\n"
        "6. Align visual tone with dialect (e.g., Telangana Telugu aesthetics).\n"
        "7. Ensure relevance for rural and multilingual Indian learners.\n"
        "8. Return both scene prompts and actual images (if model supports).\n"
        "9. Ensure visuals are suitable for display or inclusion in PDFs.\n"
        "10. Output must match the VisualOutputSchema for consistency."
    ),
    expected_output=VisualOutputSchema,
    output_json=True,
    context_injection=True
)  