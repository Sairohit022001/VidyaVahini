from tasks import Task 
from pydantic import BaseModel, Field
from typing import Optional, List

 #Define structured schema for the response
class AskMeResponseSchema(BaseModel):
    answer: str = Field(..., description="Detailed and culturally adapted answer to the user's question")
    source_context: Optional[str] = Field(None, description="Original paragraph/context used for answering")
    follow_up_question: Optional[str] = Field(None, description="Suggested follow-up or extension question")
    suggested_agents: Optional[List[str]] = Field(
        default=["CoursePlannerAgent", "BhāṣāGuru"],
        description="Downstream agents for voice narration or learning continuation"
    )
    confidence_score: Optional[float] = Field(None, description="Model's confidence in the generated answer (0-1)")

    class Config:
        title = "AskMe Agent Output Schema"
        description = "Structured output format from AskMeAgent that resolves doubts using Gemini and prior class context."


ask_question_task = Task(
    name="Resolve Classroom Doubt",
    description=(
        "Understand and interpret a classroom-level query (from teacher or student).\n"
        "Automatically retrieve prior lesson context from LessonPlannerAgent or ResearchAgent.\n"
        "Use dialect-based personalization for tone (e.g., Telangana Telugu).\n"
        "Adapt explanation complexity based on grade (simple/medium/advanced).\n"
        "Provide grounded answer (no hallucinations) with valid source context.\n"
        "Structure output with: answer, source paragraph, confidence, follow-up question.\n"
        "Suggest continuation agents like BhāṣāGuru or CoursePlannerAgent.\n"
        "Tune response for BhāṣāGuru TTS output if selected.\n"
        "Use Gemini (or other LLM) with memory and structured JSON output.\n"
        "Final output should be student-friendly, accurate, and curriculum-aligned."
    ),
    expected_output=AskMeResponseSchema,
    output_json=True,
    context_injection=True,
    output_file="outputs/ask_me_response_{timestamp}.json",
    guardrails={
        "retry_on_fail": 2,
        "fallback_response": {
            "answer": "Sorry, I couldn't generate a confident answer. Please rephrase the question.",
            "source_context": None,
            "follow_up_question": "Can you ask the question differently?",
            "confidence_score": 0.0,
            "suggested_agents": ["BhāṣāGuru"]
        }
    },
    metadata={
        "agent": "AskMeAgent",
        "audience": "Teachers and Students",
        "grade_range": "1-10 and UG",
        "dialect_support": True,
        "uses_contextual_memory": True,
        "downstream_support": ["VoiceAgent", "CoursePlannerAgent", "QuizAgent"],
    }
)

