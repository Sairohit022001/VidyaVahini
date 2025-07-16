from crewflows import Task
from pydantic import BaseModel, Field
from typing import List

class LessonOutputSchema(BaseModel):
    topic_title: str = Field(..., description="Title of the lesson topic")
    introduction: str = Field(..., description="Introductory explanation of the topic")
    core_concepts: List[str] = Field(..., description="Key concepts listed in bullet points")
    explanation: str = Field(..., description="Deep explanation with cultural relevance")
    examples: List[str] = Field(..., description="Examples for easier understanding")
    summary: str = Field(..., description="Brief summary covering all key ideas")
    suggested_agents: List[str] = Field(
        default=["QuizAgent", "StoryTellerAgent", "VisualAgent"],
        description="Agents to call next"
    )

generate_lesson_task = Task(
    name="Generate Lesson Plan",
    description=(
        "Accept topic, grade level, and dialect.\n"
        "Generate an introductory explanation.\n"
        "Identify and list all core concepts.\n"
        "Provide deep, structured explanations.\n"
        "Include at least 2 real-world examples.\n"
        "Ensure tone is adapted to grade level.\n"
        "Incorporate regional language and culture.\n"
        "Output structured JSON as per schema.\n"
        "Make output usable for quiz and story generation.\n"
        "Must be editable by teacher before finalizing."
    ),
    expected_output=LessonOutputSchema,
    output_json=True,
    context_injection=True,
    verbose=True,
    output_file="outputs/lesson_output_{timestamp}.json",
    guardrails={
        "retry_on_fail": 1,
        "fallback_response": {
            "topic_title": "Topic",
            "introduction": "Introduction not available",
            "core_concepts": [],
            "explanation": "Explanation failed",
            "examples": [],
            "summary": "Summary not generated",
            "suggested_agents": []
        }
    },
    metadata={
        "agent": "LessonPlannerAgent",
        "access": "teacher_only",
        "downstream": ["QuizAgent", "StoryTellerAgent", "VisualAgent","MultimodalResearchAgent"],
        "triggers": ["on_topic_selection"]
    }
)
