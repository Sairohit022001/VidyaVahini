# tasks/ask_me_task.py

from crewai import Task
from pydantic import BaseModel, Field
from typing import Optional

# Step 1: Define structured schema for the response
class AskMeResponseSchema(BaseModel):
    answer: str = Field(..., description="Detailed and culturally adapted answer to the user's question")
    source_context: Optional[str] = Field(None, description="Original paragraph/context used for answering")
    follow_up_question: Optional[str] = Field(None, description="Suggested follow-up or extension question")
    suggested_agents: Optional[list[str]] = Field(
        default=["CoursePlannerAgent", "BhāṣāGuru"],
        description="Downstream agents for voice narration or learning continuation"
    )
    confidence_score: Optional[float] = Field(None, description="Model's confidence in the generated answer (0-1)")

# Step 2: Define the task
ask_question_task = Task(
    name="Resolve Classroom Doubt",
    description=(
        "Interpret a student or teacher's query in the context of the current class topic. "
        "Use memory and context from previous agents (LessonPlannerAgent, ResearchAgent, etc.). "
        "Provide a clear, regionally contextual, and educational answer. "
        "Adapt complexity based on grade level: simple for classes 1–5, medium for 6–10, deep and conceptual for above grade 10. "
        "Ensure zero hallucination by grounding response in valid class material or research input. "
        "Generate a follow-up question that helps extend learning. "
        "Maintain dialectal tone when required for BhāṣāGuru narration. "
        "Use Gemini or supported LLM with contextual memory enabled."
    ),
    expected_output=AskMeResponseSchema,
    output_json=True,
    context_injection=True
)
