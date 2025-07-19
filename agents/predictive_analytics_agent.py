from crewflows import Agent
from crewflows.memory.local_memory_handler import LocalMemoryHandler
from tools.predictive_analytics_tool import PredictiveAnalyticsTool
from tasks.predictive_analytics_task import PredictiveAnalyticsTask
from langchain_google_genai import ChatGoogleGenerativeAI


# Initialize memory handler
memory_handler = LocalMemoryHandler(
    session_id="predictive_analytics_session",
    file_path="memory/predictive_analytics_memory.json"
)

# Instantiate the tool
predictive_analytics_tool = PredictiveAnalyticsTool()

class PredictiveAnalyticsAgent(Agent):
    def __init__(self):
        super().__init__(
            name="PredictiveAnalyticsAgent",
            role="""
1. Analyze student performance data to identify trends and predict learning outcomes.
2. Provide insights on class-level strengths and weaknesses.
3. Suggest personalized learning paths or interventions for individual students.
4. Help teachers identify students who may need additional support.
5. Offer data-driven recommendations for adjusting lesson plans.
6. Integrate with other agents to inform content creation and gamification strategies.
7. Ensure data privacy and security compliance.
8. Generate reports and visualizations of student progress.
9. Support early identification of learning difficulties.
10. Contribute to a data-informed educational approach.
""",
            goal="""
Provide actionable insights from student performance data to improve learning outcomes and inform teaching strategies.
""",
            backstory="""
PredictiveAnalyticsAgent serves as the data scientist for VidyaVāhinī. 
It crunches numbers from quizzes, assignments, and interactions to understand student learning patterns. 
By identifying potential challenges early on, it enables timely support and personalized learning adjustments. 
It works diligently to provide clear, understandable data visualizations and reports for teachers. 
Its mission is to use the power of data to ensure every student has the opportunity to succeed.
""",
            memory=True,
            memory_handler=memory_handler,
            allow_delegation=True,
            verbose=True,
            tools=[predictive_analytics_tool],
            tasks=[PredictiveAnalyticsTask(name=PredictiveAnalyticsTask.name, description=PredictiveAnalyticsTask.description)],
            user_type="teacher",
            metadata={
                "data_sources": "quiz results, assignments",
                "analysis_level": "class, individual"
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
        Process inputs asynchronously to generate predictive analytics.

        Args:
            inputs (dict): Should include 'quiz_results' and optional 'context_from_doc'.

        Returns:
            dict: Predictive analytics insights including average score, top performers, weak areas, and suggestions.
        """
        try:
            quiz_results = inputs.get("quiz_results", [])
            context_from_doc = inputs.get("context_from_doc", {})

            context = {
                "quiz_results": quiz_results,
                "context_from_doc": context_from_doc
            }

            # Run the predictive analytics task asynchronously
            predictive_task_instance = PredictiveAnalyticsTask(name=PredictiveAnalyticsTask.name, description=PredictiveAnalyticsTask.description)
            result = await predictive_task_instance.run(context)
            return result

        except Exception as e:
            return {"error": f"PredictiveAnalyticsAgent process() failed: {str(e)}"}

# Instantiate agent without params
predictive_analytics_agent = PredictiveAnalyticsAgent()

# Declare inputs
predictive_analytics_agent.add_input("quiz_results")
predictive_analytics_agent.add_input("context_from_doc")

# Declare outputs
predictive_analytics_agent.add_output("average_score")
predictive_analytics_agent.add_output("top_performers")
predictive_analytics_agent.add_output("weak_areas")
predictive_analytics_agent.add_output("lesson_plan_suggestions")
