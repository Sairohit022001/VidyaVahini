from tasks.base import BaseTask  # Assuming this exists in your project
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from tools.quiz_generation_tool import QuizGenerationTool

class QuizOutputSchema(BaseModel):
    topic: str = Field(..., description="Topic of the quiz based on the lesson")
    grade_level: str = Field(..., description="Target grade level for the quiz")
    questions: List[Dict[str, Any]] = Field(
        ...,
        description="List of questions with text, options, correct answer, and explanation"
    )
    format_type: str = Field(..., description="Format of quiz questions, e.g., MCQ, Fill-in-the-blank")
    total_marks: int = Field(..., description="Total marks for the quiz")
    dialect_adapted: bool = Field(..., description="Whether the questions are adapted for regional dialect")

class QuizTask(BaseTask):
    name = "Generate Quiz from Lesson"
    description = (
        "Accept lesson content and grade level, generate 5–10 questions covering core concepts, "
        "matching specified formats (MCQ, Fill-in-the-blank, Match-the-following), "
        "use age-appropriate and dialect-adapted language, include explanations, "
        "avoid trivial/repetitive questions, output JSON matching QuizOutputSchema."
    )
    expected_output = QuizOutputSchema
    output_json = True
    context_injection = True
    verbose = True
    output_file = "outputs/quiz_output_{timestamp}.json"
    guardrails = {
        "retry_on_fail": 2,
        "fallback_response": {
            "topic": "Default Topic",
            "grade_level": "Unknown",
            "questions": [],
            "format_type": "MCQ",
            "total_marks": 0,
            "dialect_adapted": False,
        }
    }
    metadata = {
        "agent": "QuizAgent",
        "access": "teacher_and_student",
        "downstream": ["CoursePlannerAgent", "GamificationAgent"],
        "triggers": ["on_lesson_completion"]
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.quiz_tool = QuizGenerationTool()

    async def run(self, inputs: dict) -> dict:
        """
        Run the quiz generation task asynchronously using the QuizGenerationTool.

        Args:
            inputs (dict): Input data containing lesson content, grade level, dialect, etc.

        Returns:
            dict: Quiz data conforming to QuizOutputSchema or fallback on failure.
        """
        try:
            result = self.quiz_tool.run(inputs)
            return result
        except Exception as e:
            return {
                **self.guardrails["fallback_response"],
                "error_details": str(e)
            }

# Instantiate for external use
quiz_task = QuizTask(name=QuizTask.name, description=QuizTask.description)
