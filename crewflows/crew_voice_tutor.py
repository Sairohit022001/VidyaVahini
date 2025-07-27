from agents.voice_tutor_agent import VoiceTutorAgent
import asyncio

async def run_voice_tutor_crew(prompt: str, dialect: str = "default") -> dict:
    agent = VoiceTutorAgent()
    response = await agent.execute(prompt, dialect)
    return response

if __name__ == "__main__":
    import asyncio
    sample_prompt = "Explain Photosynthesis for 5th grade in Telangana dialect."
    sample_dialect = "telangana"

    result = asyncio.run(run_voice_tutor_crew(sample_prompt, sample_dialect))

    print("=== SSML Output ===")
    print(result.get("ssml", "No SSML output"))
    print("\n=== Audio saved at ===")
    print(result.get("audio_file", "No audio file path"))
