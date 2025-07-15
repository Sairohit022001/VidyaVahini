"""
Voice Tutor Crew

Description:
    Orchestrates the Voice Tutor Agent workflow that converts lesson or story
    text into synthesized speech audio, tailored by dialect and student reading level.
    Integrates Google Cloud Text-to-Speech with dialect clustering and SSML prosody.

Features:
- Validates inputs for text, dialect, and student level.
- Returns base64 audio, SSML used, and voice model info.
- Logs execution steps and errors.
- Supports retry on failure and fallback response.

Usage:
    Call run_voice_tutor_crew(text, dialect, student_level) to get speech audio output.
"""

from crewai import Crew
from agents.voice_tutor_agent import voice_tutor_agent
from tasks.voice_tutor_task import voice_tutor_task

from pydantic import BaseModel, ValidationError
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(levelname)s — %(message)s")
logger = logging.getLogger(__name__)

# Setup Crew
voice_tutor_crew = Crew(
    agents=[voice_tutor_agent],
    tasks=[voice_tutor_task],
    verbose=True,
    process="sequential",
    memory=False,
)

voice_tutor_agent.add_input("text")
voice_tutor_agent.add_input("dialect")
voice_tutor_agent.add_input("student_level")

voice_tutor_agent.add_output("audio_base64")
voice_tutor_agent.add_output("ssml_used")
voice_tutor_agent.add_output("voice_model")
voice_tutor_agent.add_output("error")

# Input validation schema
class VoiceTutorInput(BaseModel):
    text: str
    dialect: str
    student_level: str

def run_voice_tutor_crew(text: str, dialect: str, student_level: str = "beginner"):
    """
    Runs the Voice Tutor Crew to generate speech audio.

    Parameters:
        text (str): Text content for synthesis.
        dialect (str): Regional dialect (e.g., Telangana Telugu).
        student_level (str): Reading level - beginner, intermediate, advanced.

    Returns:
        dict: {
            "audio_base64": str,
            "ssml_used": str,
            "voice_model": str,
            "error": Optional[str]
        }
    """
    try:
        inputs = VoiceTutorInput(text=text, dialect=dialect, student_level=student_level)
        logger.info(f"Input validated for Voice Tutor Crew: dialect={dialect}, level={student_level}")

        result = voice_tutor_crew.run(inputs=inputs.dict())
        logger.info("Voice Tutor Agent execution completed successfully")
        return result

    except ValidationError as ve:
        logger.error(f"Validation error in Voice Tutor inputs: {ve}")
        return {"error": "Invalid inputs", "details": ve.errors()}
    except Exception as e:
        logger.error(f"Voice Tutor Crew execution error: {e}")
        return {"error": "Execution failed", "details": str(e)}

if __name__ == "__main__":
    # Sample usage for local testing
    sample_text = "Photosynthesis is the process by which green plants make their food."
    sample_dialect = "Telangana Telugu"
    sample_level = "beginner"

    output = run_voice_tutor_crew(sample_text, sample_dialect, sample_level)
    print(output)
