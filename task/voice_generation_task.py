# tasks/voice_tutor_task.py

from crewai import Task
from pydantic import BaseModel, Field
from typing import Literal, Optional

class VoiceTutorInputSchema(BaseModel):
    text: str = Field(..., description="Text content to synthesize")
    dialect: str = Field(..., description="Regional dialect e.g. Telangana Telugu, Andhra Telugu")
    student_level: Literal["beginner", "intermediate", "advanced"] = Field(
        default="beginner", description="Reading level of the student"
    )

class VoiceTutorOutputSchema(BaseModel):
    audio_base64: Optional[str] = Field(None, description="Base64 encoded MP3 audio")
    ssml_used: Optional[str] = Field(None, description="SSML markup used for synthesis")
    voice_model: Optional[str] = Field(None, description="Name of the voice model used")
    error: Optional[str] = Field(None, description="Error message, if any")

voice_tutor_task = Task(
    name="VoiceTutorSpeechSynthesis",
    description=(
        "Generates speech audio from text input tailored by dialect and student reading level. "
        "Uses Google Cloud Text-to-Speech API, outputs base64 MP3 and SSML markup."
    ),
    inputs=["text", "dialect", "student_level"],
    expected_output=VoiceTutorOutputSchema,
    output_json=True,
    context_injection=True,
    verbose=True,
    output_file="outputs/voice_tutor_output_{timestamp}.json",
    guardrails={
        "retry_on_fail": 2,
        "fallback_response": {
            "audio_base64": None,
            "ssml_used": "",
            "voice_model": "",
            "error": "Fallback: speech synthesis failed"
        }
    },
    metadata={
        "agent": "VoiceTutorAgent",
        "access": "student",
        "triggers": ["on_lesson_complete", "on_request_speech"],
        "integration": "gcp_text_to_speech"
    },
    tool="VoiceTutorTool"
)
