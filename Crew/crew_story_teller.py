from agents.story_teller_agent import story_teller_agent
from tasks.story_teller_tasks import generate_story_task
from crewai import Crew
from dotenv import load_dotenv
import os

# Load .env file if needed
load_dotenv()

# Define the crew for story generation
story_teller_crew = Crew(
    agents=[story_teller_agent],
    tasks=[generate_story_task],
    verbose=True 

def run_story_generation(topic: str, grade: int, dialect: str, story_mode: str):
    """
    Runs the story generation agent workflow.
    
    Parameters:
        topic (str): Academic topic to generate a story for
        grade (int): Grade level of students
        dialect (str): Regional dialect (e.g., Telangana Telugu)
        story_mode (str): One of ['modern', 'moral', 'mythological', 'folk']
    
    Returns:
        dict: JSON output of the generated story
    """

    input_data = {
        "topic": topic,
        "grade": grade,
        "dialect": dialect,
        "story_mode": story_mode
    }

    result = story_teller_crew.run(inputs=input_data)
    return result
