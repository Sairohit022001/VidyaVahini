from crewai.crew_voice_tutor import run_voice_tutor_crew
import os
import platform
import subprocess

import os

# Set path explicitly if not already set
import os
print("Current working directory:", os.getcwd())
print("File exists:", os.path.isfile("/workspaces/VidyaVahini/keys/vidyavahini-tts-3f4de486bdd1.json"))





def play_audio(file_path):
    system = platform.system()
    if system == "Windows":
        os.startfile(file_path)
    elif system == "Darwin":
        subprocess.call(["afplay", file_path])
    else:
        try:
            subprocess.call(["mpg123", file_path])
        except FileNotFoundError:
            print("Please install mpg123 or another mp3 player to play audio.")

if __name__ == "__main__":
    prompt = "Explain the water cycle for 6th grade students in Andhra dialect."
    dialect = "andhra"

    print(f"Running Voice Tutor Test with prompt:\n{prompt}\nDialect: {dialect}\n")
    result = run_voice_tutor_crew(prompt, dialect)

    print("SSML Generated:\n", result["ssml"])
    print("Audio file path:", result["audio_file"])

    play_audio(result["audio_file"])
