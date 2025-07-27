import json
import logging

def course_planner_agent(topic: str, grade_level: int, dialect: str, pdf_lesson=None, db_lesson=None):
    """
    CoursePlannerAgent logic:
    - Check pdf_lesson and db_lesson (both optional)
    - Return lesson plan JSON if available, else error JSON
    """
    if pdf_lesson:
        # Simulate extraction/summarization from PDF
        lesson_plan = {
            "topic_title": pdf_lesson.get("title", topic),
            "introduction": pdf_lesson.get("introduction", ""),
            "core_concepts": pdf_lesson.get("core_concepts", []),
            "explanation": pdf_lesson.get("explanation", ""),
            "examples": pdf_lesson.get("examples", []),
            "summary": pdf_lesson.get("summary", "")
        }
        response = {
            "status": "success",
            "lesson_plan": lesson_plan,
            "suggested_agents": ["QuizAgent", "StoryTellerAgent"]
        }
        return response

    elif db_lesson:
        # Use DB lesson directly (assuming same format)
        response = {
            "status": "success",
            "lesson_plan": db_lesson,
            "suggested_agents": ["QuizAgent", "StoryTellerAgent"]
        }
        return response

    else:
        # No lesson source found
        response = {
            "status": "error",
            "error_message": "No PDF or Database lesson provided.",
            "suggested_agents": []
        }
        return response


# Example usage:
pdf_example = {
    "title": "Photosynthesis: How Plants Make Food",
    "introduction": "Photosynthesis is a process by which plants make food...",
    "core_concepts": ["Plants use sunlight", "Chlorophyll is essential", "Glucose and oxygen are produced"],
    "explanation": "Detailed explanation here...",
    "examples": ["Mango tree", "Neem tree"],
    "summary": "Summary of photosynthesis..."
}

result = course_planner_agent("Photosynthesis", 7, "Telangana", pdf_lesson=pdf_example)
print(json.dumps(result, indent=2))
