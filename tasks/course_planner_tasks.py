from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import asyncio

# Define the schema first
class CoursePlanSchema(BaseModel):
    current_topic: str = Field(..., description="Current topic the student or class is focused on")
    recommended_topic: str = Field(..., description="AI-suggested next logical topic to continue the course")
    reason: str = Field(..., description="Justification or rationale for selecting the next topic")
    difficulty_adjustment: str = Field(..., description="Indicates whether topic complexity is adjusted (increase/decrease/same)")
    level: str = Field(..., description="Target complexity level for the recommended topic: Beginner / Medium / Advanced")
    suggested_agents: List[str] = Field(
        default=["QuizAgent", "VisualAgent", "ContentCreatorAgent"],
        description="Downstream agents to trigger post this decision"
    )
    linked_materials: Optional[List[str]] = Field(
        default=[],
        description="Optional list of materials, PDFs, or URLs to accompany the recommended topic"
    )

    class Config:
        title = "Course Planner Output Schema"
        description = "Schema used to plan next steps in personalized learning flow"


class GenerateCoursePlanTask:
    name = "Generate Next Course Topic"
    description = (
        "Analyze the student's current topic and quiz performance.\n"
        "Identify knowledge gaps or signs of mastery.\n"
        "Suggest the next logical topic from the curriculum.\n"
        "Consider topic prerequisites and concept flow.\n"
        " Justify the chosen topic recommendation.\n"
        "Adapt difficulty level: Beginner, Medium, or Advanced.\n"
        "Align topic complexity with class/student level.\n"
        "Suggest appropriate follow-up agents.\n"
        "Optionally attach helpful reference material.\n"
        "Respond strictly in valid JSON conforming to CoursePlanSchema."
    )
    expected_output = CoursePlanSchema
    output_json = True
    context_injection = True
    verbose = True
    output_file = "outputs/course_plan_output_{timestamp}.json"
    guardrails = {
        "retry_on_fail": 1,
        "fallback_response": {
            "current_topic": "Unknown",
            "recommended_topic": "Photosynthesis",
            "reason": "Default fallback topic for curriculum flow",
            "difficulty_adjustment": "same",
            "level": "Medium",
            "suggested_agents": ["QuizAgent"],
            "linked_materials": []
        }
    }
    metadata = {
        "agent": "CoursePlannerAgent",
        "audience": "Grades 1–10 + UG",
        "access_level": "teacher_only",
        "downstream": ["QuizAgent", "StoryTellerAgent", "VisualAgent", "MultimodalResearchAgent"],
        "integration": ["StudentLevelAgent", "TeacherDashboardAgent"],
        "outputs": ["NextTopicRecommendation", "CurriculumReport", "ClassPacingGuide"]
    }

    async def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Async run method to analyze student progress and suggest next course topic.

        Args:
            inputs (dict): Expected keys include 'current_topic', 'quiz_scores', 'student_level', etc.

        Returns:
            dict: A JSON-compatible dict conforming to CoursePlanSchema.
        """
        try:
            await asyncio.sleep(0.1)  # Simulate async processing or API call

            current_topic = inputs.get("current_topic", "Unknown")
            # Example simplistic logic to pick next topic
            recommended_topic = "Photosynthesis"
            reason = "Photosynthesis is the natural next step in the biology curriculum."
            difficulty_adjustment = "same"
            level = inputs.get("student_level", "Medium")
            suggested_agents = ["QuizAgent", "VisualAgent", "ContentCreatorAgent"]
            linked_materials = inputs.get("linked_materials", [])

            response = CoursePlanSchema(
                current_topic=current_topic,
                recommended_topic=recommended_topic,
                reason=reason,
                difficulty_adjustment=difficulty_adjustment,
                level=level,
                suggested_agents=suggested_agents,
                linked_materials=linked_materials,
            )

            return response.dict()

        except Exception as e:
            fallback = self.guardrails.get("fallback_response", {})
            fallback["reason"] += f" Error details: {str(e)}"
            return fallback


# Instantiate the task object
generate_course_plan_task = GenerateCoursePlanTask()
