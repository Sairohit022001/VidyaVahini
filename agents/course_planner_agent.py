from crewflows import Agent
from crewflows.memory.local_memory_handler import LocalMemoryHandler
from typing import Dict, Any

memory_handler = LocalMemoryHandler(
    session_id="course_planner_agent_session",
    file_path="memory/course_planner_agent_memory.json"
)


class CoursePlannerAgent(Agent):
    def __init__(self, *args, name: str = "course_planner_agent", **kwargs):
        super().__init__(
            *args,
            name=name,
            role="AI agent responsible for assembling lesson plans from PDFs or database lesson data.",
            goal="Produce structured, culturally contextual lesson plans for teachers and learners.",
            backstory="CoursePlannerAgent integrates various content sources into a coherent lesson plan for VidyaVāhinī users.",
            memory=True,
            memory_handler=memory_handler,
            verbose=True,
            **kwargs
        )
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    async def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assemble a coherent lesson plan from provided PDF or DB lesson data.

        Args:
            inputs (dict): Expected keys:
                - topic (str)
                - grade_level (int or str, optional)
                - dialect (str, optional)
                - pdf_lesson (Optional[dict])
                - db_lesson (Optional[dict])

        Returns:
            dict: JSON-compliant response with lesson data or error.
        """
        topic = inputs.get("topic", "Unknown Topic")
        grade_level = inputs.get("grade_level", None)
        dialect = inputs.get("dialect", "English")
        pdf_lesson = inputs.get("pdf_lesson")
        db_lesson = inputs.get("db_lesson")

        # Optional: Typecast grade_level to int (if string)
        try:
            if grade_level is not None:
                grade_level = int(grade_level)
        except Exception:
            grade_level = None

        # Optionally log inputs or dialect usage here
        # print(f"[CoursePlannerAgent] topic='{topic}', grade_level={grade_level}, dialect='{dialect}'")

        if pdf_lesson:
            lesson_plan = {
                "topic_title": pdf_lesson.get("title", topic),
                "introduction": pdf_lesson.get("introduction", ""),
                "core_concepts": pdf_lesson.get("core_concepts", []),
                "explanation": pdf_lesson.get("explanation", ""),
                "examples": pdf_lesson.get("examples", []),
                "summary": pdf_lesson.get("summary", "")
            }
            return {
                "status": "success",
                "lesson_plan": lesson_plan,
                "suggested_agents": ["QuizAgent", "StoryTellerAgent"]
            }
        elif db_lesson:
            return {
                "status": "success",
                "lesson_plan": db_lesson,
                "suggested_agents": ["QuizAgent", "StoryTellerAgent"]
            }
        else:
            return {
                "status": "error",
                "error_message": "No PDF or Database lesson provided.",
                "suggested_agents": []
            }


course_planner_agent = CoursePlannerAgent()
