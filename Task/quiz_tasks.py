from crewai import Task
from pydantic import BaseModel, Field
from typing import List

class QuizOutputSchema(BaseModel):
    topic: str = Field(..., description="Topic of the quiz")
    grade_level: str = Field(..., description="Grade level for which quiz is generated")
    dialect: str = Field(..., description="Regional dialect used for question phrasing")
    questions: List[str] = Field(..., description="List of quiz questions")
    options: List[List[str]] = Field(..., description="Options per question if applicable")
    correct_answers: List[str] = Field(..., description="Correct answers per question")
    explanation: List[str] = Field(..., description="Optional explanations per question")
    mode: str = Field(..., description="Quiz mode: MCQ / FillBlanks / TrueFalse")
    retry_logic: bool = Field(..., description="Whether retry logic is enabled")

generate_quiz_task = Task(
    name="Generate Adaptive Quiz",
    description=(
        "Generate a culturally localized and adaptive quiz based on lesson content, story context, and visuals.\n"
        "The questions must be aligned with the grade level and dialect. Include at least 5 questions with answer keys.\n"
        "Support different quiz modes and retry logic for wrong attempts.\n"
        "Ensure the quiz fits curriculum standards and output follows QuizOutputSchema."
    ),
    expected_output=QuizOutputSchema,
    output_json=True,
    context_injection=True
)
