from tasks import Task
from pydantic import BaseModel, Field
from typing import List, Optional

class QuizOutputSchema(BaseModel):
    topic: str = Field(..., description="Topic of the quiz based on the lesson")
    grade_level: str = Field(..., description="Target grade level for the quiz")
    questions: List[dict] = Field(
        ...,
        description="List of question dictionaries each containing question text, options, correct answer, and explanation"
    )
    format_type: str = Field(..., description="Format of quiz questions, e.g., MCQ, Fill-in-the-blank, Match-the-following")
    total_marks: int = Field(..., description="Total marks for the quiz")
    dialect_adapted: bool = Field(..., description="Indicates if the questions are adapted for regional dialect")

generate_quiz_task = Task(
    name="Generate Quiz from Lesson",
    description=(
        "Accept lesson content and grade level.\n"
        "Generate 5–10 questions covering core concepts.\n"
        "Ensure question formats match the specified format_type (MCQ, Fill-in-the-blank, Match-the-following).\n"
        "Use age-appropriate and dialect-adapted language.\n"
        "Include explanations for each answer.\n"
        "Maintain alignment with curriculum standards.\n"
        "Avoid repetition and trivial questions.\n"
        "Output JSON following the QuizOutputSchema.\n"
        "Ensure questions are auto-gradable."
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
