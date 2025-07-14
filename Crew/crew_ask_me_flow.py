# crew/crew_ask_me_flow.py

from crewai import Crew
from agents.ask_me_agent import ask_me_agent
from tasks.ask_me_task import ask_question_task

# Optional: Load environment variables if not already loaded
from dotenv import load_dotenv
load_dotenv()

# Step 1: Create the Crew
ask_me_crew = Crew(
    agents=[ask_me_agent],
    tasks=[ask_question_task],
    verbose=True,
    process=ask_me_agent,  # Single-agent process
)

# Step 2: Define the runner function
def run_ask_me_flow(question: str, context: str = ""):
    """
    Entry point for AskMeAgent to answer a classroom doubt.
    
    Parameters:
    - question (str): The user's query
    - context (str): Lesson context or reference material
    
    Returns:
    - dict: JSON-compatible answer with follow-up and metadata
    """
    inputs = {
        "question": question,
        "context": context,
    }
    return ask_me_crew.run(inputs)
