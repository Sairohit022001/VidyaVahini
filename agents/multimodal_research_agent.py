from crewflows import Agent
from crewflows.memory import MemoryHandler
from crewflows.tools.multimodal_research_tool import multimodal_research_tool
from crewflows.tasks.multimodal_research_task import generate_multimodal_references_task


memory_handler = MemoryHandler(
    session_id="multimodal_research_session",
    file_path="memory/multimodal_research_memory.json"
)

multimodal_research_agent = Agent(
    name="MultimodalResearchAgent",
    role="Resource aggregator for in-depth topic understanding",
    goal=(
        "Given a topic/chapter or a pdf corresponding to the topic and grade level, return references from research papers, video links, and other resources "
        "to help understand the topic in depth. Tailor resources for grades 1-10, 11-12, and undergraduate studies."
        "Ensure resources are credible and relevant, covering academic papers, educational videos, and trusted websites."
        "Support teachers in finding high-quality, multimodal resources for any topic or chapter."
    ),
    backstory=(
        "This agent supports teachers by finding high-quality, multimodal resources for any topic or chapter. "
        "It searches academic databases, educational video platforms, and trusted websites, ensuring grade-appropriate recommendations."
        "The agent is designed to assist educators in enhancing their lesson plans with credible and diverse resources, "
        "making it easier to deliver comprehensive and engaging content to students."
        "includes from video lectures to academic papers, ensuring a well-rounded understanding of the subject matter."
    ),
    memory=True,
    memory_handler=memory_handler,
    allow_delegation=True,
    verbose=True,
    tools=[multimodal_research_tool],
    tasks=[generate_multimodal_references_task],
    user_type="teacher",
    metadata={
        "resource_types": "papers, videos, websites",
        "grade_levels": "1-10, 11-12, UG"
    },
    llm_config={"model": "gemini-pro", "temperature": 0.5},
    respect_context_window=True,
    code_execution_config={"enabled": True},
)

multimodal_research_agent.add_input("topic")
multimodal_research_agent.add_input("level")
multimodal_research_agent.add_input("context_from_doc")
