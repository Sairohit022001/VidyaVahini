from pydantic import BaseModel, Field
from typing import List, Dict, Any
import asyncio

class ContentCreationOutput(BaseModel):
    title: str = Field(..., description="Title of the blended lesson content")
    combined_lesson: str = Field(..., description="Final AI-enhanced lesson with structure: intro, explanation, summary, quiz")
    teacher_notes_used: List[str] = Field(..., description="List of teacher notes that were integrated into the output")

    class Config:
        title = "Content Creation Output Schema"
        description = "Schema representing AI-enhanced, blended educational material including teacher notes."

class GenerateContentTask:
    name = "Generate Blended Lesson Content"
    description = (
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
    )
    expected_output = ContentCreationOutput
    output_json = True
    context_injection = True
    verbose = True
    output_file = "outputs/content_creation_output_{timestamp}.json"
    guardrails = {
        "retry_on_fail": 2,
        "fallback_response": {
            "title": "Untitled Lesson",
            "combined_lesson": "Content creation failed. Please try again or check input notes.",
            "teacher_notes_used": []
        }
    }
    metadata = {
        "agent": "ContentCreatorAgent",
        "audience": "Teachers (Grades 1–10 and UG)",
        "access_level": "teacher_only",
        "downstream_support": ["VisualAgent", "VoiceTutorAgent", "QuizAgent"],
        "output_type": "blended_lesson",
        "editable_by_user": True
    }

    async def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Async run method to create blended lesson content combining AI and teacher notes.

        Args:
            inputs (dict): Expected keys like 'teacher_notes', 'lesson_topic', 'grade_level', 'dialect'.

        Returns:
            dict: Output structured as per ContentCreationOutput schema.
        """
        try:
            # Simulate async processing delay (replace with actual AI calls)
            await asyncio.sleep(0.1)

            teacher_notes = inputs.get("teacher_notes", [])
            lesson_topic = inputs.get("lesson_topic", "Untitled Topic")
            grade_level = inputs.get("grade_level", "medium")
            dialect = inputs.get("dialect", "default")

            # Dummy content generation logic (replace with your real AI generation)
            combined_lesson = (
                f"# {lesson_topic}\n\n"
                "## Introduction\n"
                "This lesson introduces key concepts...\n\n"
                "## Explanation\n"
                "Detailed explanation goes here...\n\n"
                "## Summary\n"
                "Key points summarized.\n\n"
                "## Quiz\n"
                "1. Question one?\n"
                "2. Question two?\n"
            )

            response = ContentCreationOutput(
                title=lesson_topic,
                combined_lesson=combined_lesson,
                teacher_notes_used=teacher_notes
            )
            return response.dict()

        except Exception as e:
            fallback = self.guardrails.get("fallback_response", {})
            fallback["combined_lesson"] += f" Error details: {str(e)}"
            return fallback

# Create instance for agent use
generate_content_task = GenerateContentTask()
