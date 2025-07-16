from crewflows import Task
from pydantic import BaseModel, Field
from typing import List, Optional

class QuizOutputSchema(BaseModel):
    topic: str
    grade_level: str
    questions: List[dict] = Field(..., description="List of question dictionaries with question, options, answer, explanation")
    format_type: str = Field(..., description="MCQ / Fill-in-the-blank / Match-the-following")
    total_marks: int = Field(..., description="Total marks")
    dialect_adapted: bool = Field(..., description="Indicates if question is adapted for dialect")

generate_quiz_task = Task(
    name="Generate Quiz from Lesson",
    description=(
        "Accept lesson content and grade level.\n"
        "Generate 5–10 questions based on core concepts.\n"
        "Questions must match format_type (MCQ / Fill-in / Match).\n"
        "Ensure age-appropriate language.\n"
        "Include explanations for answers.\n"
        "Adapt questions for provided dialect.\n"
        "Ensure curriculum alignment.\n"
        "Avoid repetition or trivial questions.\n"
        "Use JSON output following schema.\n"
        "Questions should be auto-gradable."
    ),
    expected_output=QuizOutputSchema,
    output_json=True,
    context_injection=True,
    verbose=True,
    output_file="outputs/quiz_output_{timestamp}.json",
    guardrails={
        "retry_on_fail": 2,
        "fallback_response": {
            "topic": "Default Topic",
            "grade_level": "Unknown",
            "questions": [],
            "format_type": "MCQ",
            "total_marks": 0,
            "dialect_adapted": False
        }
    },
    metadata={
        "agent": "QuizAgent",
        "access": "teacher_and_student",
        "downstream": ["CoursePlannerAgent", "GamificationAgent"],
        "triggers": ["on_lesson_completion"]
    }
)

