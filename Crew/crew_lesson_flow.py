from crewai import Crew
from agents.lesson_planner_agent import lesson_planner_agent
from tasks.lesson_planner_tasks import lesson_generation_task

from dotenv import load_dotenv
import os

# Load .env file if needed
load_dotenv()

# ✅ Build the crew
lesson_crew = Crew(
    agents=[lesson_planner_agent],
    tasks=[lesson_generation_task],
    verbose=True,
    process="sequential",   # Optionally change to "hierarchical" or "async" if needed
)

def run_lesson_crew(topic: str, level: str, dialect: str):
    print("🚀 Running Lesson Planner Agent Crew...\n")

    # ✅ Send inputs via context
    results = lesson_crew.kickoff(
        inputs={
            "topic": topic,
            "level": level,
            "dialect": dialect
        }
    )

    return results
