from agents.voice_tutor_agent import VoiceTutorAgent

def run_voice_tutor_crew(prompt: str, dialect: str = "default") -> dict:
    """
    Orchestrate the Voice Tutor agent for a given prompt and dialect.

    Args:
        prompt (str): The text input to generate speech from.
        dialect (str): Dialect choice ('telangana', 'andhra', 'default').

    Returns:
        dict: {
            "ssml": SSML string,
            "audio_file": path to generated audio file,
            "dialect": dialect used
        }
    """
    agent = VoiceTutorAgent()
    response = agent.execute(prompt, dialect)
    return response


if __name__ == "__main__":
    sample_prompt = "Explain Photosynthesis for 5th grade in Telangana dialect."
    sample_dialect = "telangana"

    result = run_voice_tutor_crew(sample_prompt, sample_dialect)

    print("=== SSML Output ===")
    print(result["ssml"])
    print("\n=== Audio saved at ===")
    print(result["audio_file"])
