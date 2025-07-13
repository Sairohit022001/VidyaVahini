from crewai import Task
from pydantic import BaseModel, Field
from typing import List, Optional

# Define the schema for the lesson output
class LessonOutputSchema(BaseModel):
    topic_title: str = Field(..., description="Title of the lesson topic")
    introduction: str = Field(..., description="Detailed introduction to the topic")
    core_concepts: List[str] = Field(..., description="List of all important core concepts explained")
    explanation: str = Field(..., description="Detailed Full-length explanation of the topic")
    examples: Optional[List[str]] = Field(default=[], description="Real-life examples and most suitable examples to explain concepts")
    summary: str = Field(..., description="A concise points wise summary of the topic")
    suggested_agents: List[str] = Field(
        default=["QuizAgent", "StoryTellerAgent", "VisualAgent"],
        description="Agents recommended to continue this flow"
    )

# Task for generating a lesson plan    
generate_lesson_task = Task(
    name="Generate Lesson Plan",
    description=(
        "Generate a full lesson plan for a given topic, level, language and grade. "
        "Include an introduction, key concepts, deep explanation, real-world examples, and summary. "
        "Output must follow the LessonOutputSchema JSON structure. "
        "Use simple language if grade level is below 6. "
        "Use medium level technical language if grade level is above 6 to 10. "
        "Use advanced technical language if grade level is above 10. "
        "Ensure cultural and regional relevance using the dialect provided."
        "The output should be suitable for educational purposes and ready for use in a lesson plan by a teacher."
    ),
    expected_output=LessonOutputSchema,
    output_json=True,  # ✅ Important for UI and downstream agents
    context_injection=True,
)