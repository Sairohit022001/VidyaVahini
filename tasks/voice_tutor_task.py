import asyncio
from typing import Dict
from tools.voice_tutor_tool import VoiceTutorTool

class VoiceTutorTask:
    def __init__(self):
        self.tool = VoiceTutorTool()

    async def run(self, input_text: str, dialect: str = "default") -> Dict[str, str]:
        loop = asyncio.get_running_loop()
        try:
            # Run synchronous tool method in thread executor to avoid blocking
            result = await loop.run_in_executor(None, self.tool.generate_voice_tutor, input_text, dialect)
            return result
        except Exception as e:
            raise RuntimeError(f"VoiceTutorTask failed: {str(e)}") from e
