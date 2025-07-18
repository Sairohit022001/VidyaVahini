from tasks import Task
from pydantic import BaseModel, Field
from typing import List

# Define structured schema for multimodal references output
class MultimodalReferencesOutput(BaseModel):
    research_papers: List[str] = Field(..., description="List of relevant research paper URLs or citations")
    video_links: List[str] = Field(..., description="List of curated educational video URLs")
    trusted_websites: List[str] = Field(..., description="List of credible websites with relevant content")

generate_multimodal_references_task = Task(
    name="GenerateMultimodalReferences",
    description=(
        "Given a topic or chapter and a grade level, retrieve curated multimodal references.\n"
        "Include academic research papers, educational videos, and trusted websites.\n"
        "Ensure recommendations are grade-appropriate and credible.\n"
        "Support for grades 1-10, 11-12, and undergraduate levels."
    ),
    inputs=["topic", "grade"],
    expected_output=MultimodalReferencesOutput,
    output_json=True,
    verbose=True,
    tool="multimodal_research_tool",
    guardrails={
        "retry_on_fail": 2,
        "fallback_response": {
            "research_papers": [],
            "video_links": [],
            "trusted_websites": []
        }
    },
    metadata={
        "agent": "MultimodalResearchAgent",
        "access": "teacher_only",
        "downstream": ["LessonPlannerAgent", "ContentCreatorAgent"],
        "audience": "Grades 1-10, 11-12, UG",
        "output_type": "references"
    }
)
