from crew.crew_voice_tutor import run_voice_tutor_crew

if __name__ == "__main__":
    sample_text = "Photosynthesis is the process by which green plants make their food."
    sample_dialect = "Telangana Telugu"
    sample_level = "beginner"

    output = run_voice_tutor_crew(sample_text, sample_dialect, sample_level)
    print("Voice Tutor Output:")
    print(output)
