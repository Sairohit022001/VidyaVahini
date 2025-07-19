from tasks.base import BaseTask  # assuming this is your base class
from pydantic import BaseModel, Field
from typing import List

class MultimodalReferencesOutput(BaseModel):
    research_papers: List[str]
    video_links: List[str]
    trusted_websites: List[str]

class MultimodalResearchTask(BaseTask):
    name = "GenerateMultimodalReferences"
    description = (
        "Given a topic and grade, return multimodal references such as research papers, videos, and trusted websites."
    )
    inputs = ["topic", "grade"]
    output_model = MultimodalReferencesOutput
    output_json = True

    async def run(self, input_data):
        topic = input_data["topic"]
        grade = input_data["grade"]

        # Replace with real multimodal reference logic
        result = {
            "research_papers": [f"https://scholar.google.com/{topic}"],
            "video_links": [f"https://youtube.com/results?search_query={topic}+class+{grade}"],
            "trusted_websites": [f"https://www.khanacademy.org/search?page_search_query={topic}"]
        }
        return result
