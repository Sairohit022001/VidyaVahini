from crewai import Task
from pydantic import BaseModel, Field
from typing import List

class ContentCreationOutput(BaseModel):
    title: str
    combined_lesson: str
    teacher_notes_used: List[str]

generate_content_task = Task(
    name="Generate Blended Lesson Content",
    description=(
        "1. Accept input documents or teacher-written notes.\n"
        "2. Combine teacher notes with AI-generated lesson content.\n"
        "3. Maintain structure: intro, explanation, summary, quiz.\n"
        "4. Respect regional dialect and grade level tone.\n"
        "5. Ensure originality and clarity in AI content.\n"
        "6. Simplify complex ideas for lower grades.\n"
        "7. Highlight important teacher-specified topics.\n"
        "8. Return formatted markdown/text + metadata.\n"
        "9. Save draft or publish directly to student dashboard.\n"
        "10. Output content ready for visual or voice generation."
    ),
    expected_output=ContentCreationOutput,
    output_json=True,
    context_injection=True,
    verbose=True
)