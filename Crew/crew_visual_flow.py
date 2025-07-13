from crewai import Crew, Process
from agents.visual_agent import visual_agent
from tasks.visual_generation_task import generate_visual_task
from tools.visual_generation_tool import VisualGenerationTool

from dotenv import load_dotenv
load_dotenv()  

visual_tool = VisualGenerationTool()

# Attach the tool to the agent
visual_agent.tools = [visual_tool]
visual_agent.allow_delegation = False 

# ✅ Build Crew (single agent crew)
crew_visual = Crew(
    agents=[visual_agent],
    tasks=[generate_visual_task],
    process=Process.sequential,
    verbose=True,
    full_output=True  

if __name__ == "__main__":
    inputs = {
        "topic": "Photosynthesis",
        "age_group": "6–10 years",
        "dialect": "Telangana Telugu",
        "visual_type": "cartoon"
    }
    result = crew_visual.run(inputs=inputs)
    print(result)