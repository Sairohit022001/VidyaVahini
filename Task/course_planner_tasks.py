from crewai import Task
from pydantic import BaseModel, Field
from typing import List, Optional

# Step 1: Define output schema
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

# Step 2: Define task
generate_course_plan_task = Task(
    name="Generate Next Course Topic",
    description=(
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
    ),
    expected_output=CoursePlanSchema,
    output_json=True,
    context_injection=True,
    verbose=True,
    output_file="outputs/course_plan_output_{timestamp}.json",
    guardrails={
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
    },
    metadata={
        "agent": "CoursePlannerAgent",
        "audience": "Grades 1–10 + UG",
        "access_level": "teacher_only",
        "downstream": ["QuizAgent", "StoryTellerAgent", "VisualAgent", "MultimodalResearchAgent"],
        "integration": ["StudentLevelAgent", "TeacherDashboardAgent"],
        "outputs": ["NextTopicRecommendation", "CurriculumReport", "ClassPacingGuide"]
    }
)
