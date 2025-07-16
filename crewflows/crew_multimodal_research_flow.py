"""
Module: Multimodal Research Crew

Description:
    Manages the Multimodal Research Agent responsible for aggregating,
    analyzing, and generating knowledge from multiple data sources such as
    PDFs, videos, audio, and other media formats.

Features:
- Validates inputs related to research materials or query parameters.
- Supports multimodal data fusion for enhanced content generation.
- Logs progress and handles errors gracefully.

Usage:
    Invoke `run_multimodal_research_crew()` with research query or data inputs
    to obtain integrated research insights and structured outputs.
"""

from crewflows import Crew
from agents.multimodal_research_agent import multimodal_research_agent
from tasks.multimodal_research_task import multimodal_research_task

from pydantic import BaseModel, ValidationError, Field
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(levelname)s — %(message)s")
logger = logging.getLogger(__name__)

# Crew setup
multimodal_research_crew = Crew(
    agents=[multimodal_research_agent],
    tasks=[multimodal_research_task],
    verbose=True,
    process="sequential",
    memory=True
)

multimodal_research_agent.add_input("research_query")
multimodal_research_agent.add_output("aggregated_insights")
multimodal_research_agent.add_output("referenced_sources")
multimodal_research_agent.add_output("generated_summary")

# Input validation schema
class ResearchQueryInput(BaseModel):
    research_query: str = Field(..., min_length=1, description="Research query or topic")

def run_multimodal_research_crew(research_query: str):
    """
    Runs the Multimodal Research Crew to generate insights from diverse data.

    Parameters:
        research_query (str): Topic or query string for research.

    Returns:
        dict: Aggregated insights, references, summaries, or error details.
    """
    try:
        inputs = ResearchQueryInput(research_query=research_query)
        logger.info(f"Validated research query input")
        result = multimodal_research_crew.run(inputs=inputs.dict())
        logger.info("Multimodal Research Agent completed successfully")
        return result
    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        return {"error": "Invalid input", "details": ve.errors()}
    except Exception as e:
        logger.error(f"Execution error: {e}")
        return {"error": "Execution failed", "details": str(e)}

if __name__ == "__main__":
    output = run_multimodal_research_crew("Machine Learning in Education")
    print(output)
