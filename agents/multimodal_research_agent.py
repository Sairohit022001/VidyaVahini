from crewflows import Agent
from crewflows.memory.local_memory_handler import LocalMemoryHandler
from tools.multimodal_research_tool import MultimodalResearchTool
from tasks.multimodal_research_task import MultimodalResearchTask
from langchain_google_genai import ChatGoogleGenerativeAI


# Initialize memory handler
memory_handler = LocalMemoryHandler(
    session_id="multimodal_research_session",
    file_path="memory/multimodal_research_memory.json"
)

# Instantiate the tool
multimodal_research_tool = MultimodalResearchTool()

class MultimodalResearchAgent(Agent):
    def __init__(self):
        super().__init__(
            name="MultimodalResearchAgent",
            role="""
1. Aggregate multimodal academic and educational resources for any topic.
2. Search across papers, video lectures, and credible websites.
3. Tailor resources for diverse educational levels: grades 1-10, 11-12, and UG.
4. Ensure all resources are vetted for quality and relevance.
5. Support teachers with ready-to-use references for lesson enrichment.
6. Enable exploration of deep, research-backed materials.
7. Provide quick links and summaries for each resource.
8. Work with LessonPlannerAgent to integrate references into lessons.
9. Adapt recommendations based on regional dialects and curriculum needs.
10. Assist in offline-friendly content preparation with downloadable references.
""",
            goal="""
Given a topic and education level, provide high-quality multimodal research resources including papers, videos, and trusted websites for lesson enrichment.
""",
            backstory="""
MultimodalResearchAgent acts as a trusted educational librarian for VidyaVāhinī. 
It bridges classroom teaching and academic research by delivering curated resources. 
The agent scans multiple databases and video platforms, focusing on quality and grade appropriateness. 
Its mission is to empower teachers with diverse, multimodal materials to enhance student learning. 
It adapts to curriculum changes, regional languages, and offline teaching requirements. 
By integrating seamlessly with other agents, it supports a holistic educational experience.
""",
            memory=True,
            memory_handler=memory_handler,
            allow_delegation=True,
            verbose=True,
            tools=[multimodal_research_tool],
            tasks=[MultimodalResearchTask(name=MultimodalResearchTask.name, description=MultimodalResearchTask.description)],
            user_type="teacher",
            metadata={
                "resource_types": "papers, videos, websites",
                "grade_levels": "1-10, 11-12, UG"
            },
            llm=ChatGoogleGenerativeAI(
            model="models/gemini-2.5-pro",
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.3
            ),
            respect_context_window=True,
            code_execution_config={"enabled": True, "executor_type": "kirchhoff-async"},
        )

    async def process(self, inputs: dict):
        """
        Process inputs asynchronously to generate multimodal research references.

        Args:
            inputs (dict): Should include 'topic', 'grade', and optional 'context_from_doc'.

        Returns:
            dict: Research resources including papers, videos, and trusted websites.
        """
        try:
            topic = inputs.get("topic")
            grade = inputs.get("grade")
            context_from_doc = inputs.get("context_from_doc", {})

            context = {
                "topic": topic,
                "grade": grade,
                "context_from_doc": context_from_doc
            }

            # Run the research task asynchronously
            multimodal_task_instance = MultimodalResearchTask(name=MultimodalResearchTask.name, description=MultimodalResearchTask.description)
            result = await multimodal_task_instance.run(context)
            return result

        except Exception as e:
            return {"error": f"MultimodalResearchAgent process() failed: {str(e)}"}

# Instantiate agent without params
multimodal_research_agent = MultimodalResearchAgent()

# Declare inputs
multimodal_research_agent.add_input("topic")
multimodal_research_agent.add_input("grade")
multimodal_research_agent.add_input("context_from_doc")

# Declare outputs
multimodal_research_agent.add_output("research_papers")
multimodal_research_agent.add_output("video_links")
multimodal_research_agent.add_output("trusted_websites")
