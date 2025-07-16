from crewflows import Task
from pydantic import BaseModel, Field
from typing import List

# Step 1: Define structured output schema
class ContentCreationOutput(BaseModel):
    title: str = Field(..., description="Title of the blended lesson content")
    combined_lesson: str = Field(..., description="Final AI-enhanced lesson with structure: intro, explanation, summary, quiz")
    teacher_notes_used: List[str] = Field(..., description="List of teacher notes that were integrated into the output")

    class Config:
        title = "Content Creation Output Schema"
        description = "Schema representing AI-enhanced, blended educational material including teacher notes."

# Step 2: Define the task
generate_content_task = Task(
    name="Generate Blended Lesson Content",
    description=(
        "Accept input documents or teacher-written notes.\n"
        "Combine teacher notes with AI-generated lesson content.\n"
        "Maintain educational structure: intro, explanation, summary, quiz.\n"
        "Ensure regional dialect support and grade-level tone.\n"
        "Avoid plagiarism; produce original and clear AI content.\n"
        "Simplify advanced concepts for primary and middle school.\n"
        "Emphasize teacher-prioritized subtopics and notes.\n"
        "Format output in Markdown/Text for easy frontend rendering.\n"
        "Support export to visual generation or BhāṣāGuru audio.\n"
        "Provide final result as JSON-compliant output for UI + storage."
    ),
    expected_output=ContentCreationOutput,
    output_json=True,
    context_injection=True,
    verbose=True,
    output_file="outputs/content_creation_output_{timestamp}.json",
    guardrails={
        "retry_on_fail": 2,
        "fallback_response": {
            "title": "Untitled Lesson",
            "combined_lesson": "Content creation failed. Please try again or check input notes.",
            "teacher_notes_used": []
        }
    },
    metadata={
        "agent": "ContentCreatorAgent",
        "audience": "Teachers (Grades 1–10 and UG)",
        "access_level": "teacher_only",
        "downstream_support": ["VisualAgent", "VoiceTutorAgent", "QuizAgent"],
        "output_type": "blended_lesson",
        "editable_by_user": True
    }
)