"""
Crew: GamificationAgent Orchestration

This crew manages gamification logic by processing inputs from QuizAgent, LessonPlannerAgent,
and ContentCreatorAgent to generate engagement metrics like XP, badges, and leaderboards.

Flow:
- Triggered after users complete lessons, quizzes, or content creation.
- Combines inputs to calculate XP distribution, assign badges, and update leaderboard.

Memory:
- Uses CrewAI memory to track user progress and historical achievements.

Parallelism:
- Can run asynchronously alongside lesson, quiz, and story generation crews without blocking.

Inputs:
- QuizAgent (dict): Quiz completion data and scores
- LessonPlannerAgent (dict): Lesson completion status
- ContentCreatorAgent (dict): User-generated content contributions

Outputs:
- XPDistribution (dict): Experience points awarded to users
- BadgesEarned (list): Badges earned based on milestones
- LeaderboardData (list): Current leaderboard rankings
"""
from crewai import Crew
from agents.gamification_agent import gamification_agent
from tasks.gamification_task import gamification_task

from pydantic import BaseModel, ValidationError
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(levelname)s — %(message)s")
logger = logging.getLogger(__name__)

crew_gamification_flow = Crew(
    agents=[gamification_agent],
    tasks=[gamification_task],
    verbose=True,
    process="sequential",
    memory=True
)

gamification_agent.add_input("QuizAgent")
gamification_agent.add_input("LessonPlannerAgent")
gamification_agent.add_input("ContentCreatorAgent")

gamification_agent.add_output("XPDistribution")
gamification_agent.add_output("BadgesEarned")
gamification_agent.add_output("LeaderboardData")

class GamificationInput(BaseModel):
    QuizAgent: dict
    LessonPlannerAgent: dict
    ContentCreatorAgent: dict

def run_gamification_crew(quiz_data, lesson_data, content_data):
    try:
        inputs = GamificationInput(
            QuizAgent=quiz_data,
            LessonPlannerAgent=lesson_data,
            ContentCreatorAgent=content_data
        )
        logger.info(f"Validated inputs: {inputs.dict()}")
        result = crew_gamification_flow.run(inputs=inputs.dict())
        logger.info("Gamification Agent completed successfully")
        return result
    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        return {"error": "Invalid input", "details": ve.errors()}
    except Exception as e:
        logger.error(f"Execution error: {e}")
        return {"error": "Execution failed", "details": str(e)}

if __name__ == "__main__":
    sample_quiz_data = {"user1": {"score": 80, "completed": True}}
    sample_lesson_data = {"user1": {"lesson_id": 101, "completed": True}}
    sample_content_data = {"user1": {"posts_created": 3}}

    output = run_gamification_crew(sample_quiz_data, sample_lesson_data, sample_content_data)
    print(output)
