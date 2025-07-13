import os
from crewai import Crew
from agents.quiz_agent import quiz_agent
from tasks.quiz_tasks import generate_quiz_task
from tools.quiz_generation_tool import QuizGenerationTool
from dotenv import load_dotenv

load_dotenv()

# Tool setup
quiz_tool = QuizGenerationTool()
generate_quiz_task.run = quiz_tool.run

# Quiz crew
quiz_crew = Crew(
    agents=[quiz_agent],
    tasks=[generate_quiz_task],
    verbose=True,
    process_name="Quiz Flow Pipeline"
)

if __name__ == "__main__":
    input_data = {
        "topic": "Photosynthesis",
        "level": "Medium",
        "dialect": "Telangana Telugu",
        "story_context": "Story about a village farmer and crops"
    }
    result = quiz_crew.run(input_data)
    print("\n[🎯 QUIZ FLOW RESULT]\n")
    print(result)
