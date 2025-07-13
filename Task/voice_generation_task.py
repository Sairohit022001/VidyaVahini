from crewai import Task
from pydantic import BaseModel, Field

# ✅ Step 1: Define the expected JSON schema
class VoiceOutputSchema(BaseModel):
    original_text: str = Field(..., description="Original content to be voiced (lesson, story, or quiz)")
    dialect: str = Field(..., description="Dialect used to generate region-specific SSML")
    ssml_output: str = Field(..., description="Final SSML-enhanced voice markup text")
    voice_model: str = Field(..., description="The TTS model used (e.g., hi-IN-Wavenet-C)")
    audio_link: str = Field(..., description="URL to the generated TTS audio file (or base64-encoded string if offline)")
    source_agent: str = Field(..., description="Which agent triggered this voice output (e.g., 'StoryTellerAgent')")

# ✅ Step 2: Define the voice generation task
generate_voice_task = Task(
    name="Generate Voice with SSML",
    description=(
        "Convert the given educational text (lesson, story, or quiz) into regionalized SSML format "
        "based on the provided dialect. Use appropriate prosody and voice selection rules. "
        "Send the SSML to TTS engine (e.g., Google TTS or Sarvam) and return an audio file or link. "
        "Ensure the voice is educational, engaging, and appropriate for the student's age and grade. "
        "Adapt speed and tone for primary vs. senior grades. "
        "The output should strictly follow the VoiceOutputSchema JSON format."
    ),
    expected_output=VoiceOutputSchema,
    output_json=True,
    context_injection=True
)