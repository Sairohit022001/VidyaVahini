from crewai import Agent
#from crewai.memory import MemoryHandler  # REMOVE this import
from tools.voice_tutor_tool import VoiceTutorTool
from tasks.voice_tutor_task import voice_tutor_task

class VoiceTutorToolWrapper:
    name = "VoiceTutorTool"
    description = "Synthesizes speech from text using GCP Text-to-Speech with dialect and student level tuning"

    def __init__(self, tool_impl: VoiceTutorTool):
        self.tool_impl = tool_impl

    def run(self, **kwargs):
        return self.tool_impl.run(**kwargs)

voice_tutor_tool_impl = VoiceTutorTool()
voice_tutor_tool = VoiceTutorToolWrapper(voice_tutor_tool_impl)

# Remove MemoryHandler usage for now
voice_tutor_agent = Agent(
    name="VoiceTutorAgent",
    role="Converts lesson text into speech audio tailored by dialect and student reading level.",
    backstory=(
        "This agent uses Google Cloud Text-to-Speech to generate voice audio tailored to "
        "regional Telugu dialects and student reading levels (beginner, intermediate, advanced). "
        "It produces SSML markup with prosody tuning and returns base64 encoded MP3 audio."
    ),
    memory=False,  # disable memory for now
    # memory_handler=None,  # remove this line
    tools=[voice_tutor_tool],
    tasks=[voice_tutor_task],
    user_type="student",
    metadata={
        "agent_type": "voice_tutor",
        "integration": "gcp_text_to_speech",
        "dialects_supported": ["Telangana", "Andhra", "Rayalaseema"],
        "output_format": "base64_mp3"
    },
    llm_config={"model": "gemini-pro", "temperature": 0.3},
    respect_context_window=True,
    code_execution_config={
        "enabled": True,
        "executor_type": "kirchhoff-async"
    }
)

