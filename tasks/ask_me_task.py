from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import asyncio

# Define structured schema for the response
class AskMeResponseSchema(BaseModel):
    answer: str = Field(..., description="Detailed and culturally adapted answer to the user's question")
    source_context: Optional[str] = Field(None, description="Original paragraph/context used for answering")
    follow_up_question: Optional[str] = Field(None, description="Suggested follow-up or extension question")
    suggested_agents: Optional[List[str]] = Field(
        default=["CoursePlannerAgent", "BhāṣāGuru"],
        description="Downstream agents for voice narration or learning continuation"
    )
    confidence_score: Optional[float] = Field(None, description="Model's confidence in the generated answer (0-1)")

    class Config:
        title = "AskMe Agent Output Schema"
        description = "Structured output format from AskMeAgent that resolves doubts using Gemini and prior class context."

class AskMeTask:
    """
    Task to process a classroom-level question asynchronously,
    retrieving context, invoking LLM, and returning structured output.
    """
    name = "Resolve Classroom Doubt"
    description = (
        "Understand and interpret a classroom-level query (from teacher or student).\n"
        "Automatically retrieve prior lesson context from LessonPlannerAgent or ResearchAgent.\n"
        "Use dialect-based personalization for tone (e.g., Telangana Telugu).\n"
        "Adapt explanation complexity based on grade (simple/medium/advanced).\n"
        "Provide grounded answer (no hallucinations) with valid source context.\n"
        "Structure output with: answer, source paragraph, confidence, follow-up question.\n"
        "Suggest continuation agents like BhāṣāGuru or CoursePlannerAgent.\n"
        "Tune response for BhāṣāGuru TTS output if selected.\n"
        "Use Gemini (or other LLM) with memory and structured JSON output.\n"
        "Final output should be student-friendly, accurate, and curriculum-aligned."
    )
    expected_output = AskMeResponseSchema
    output_json = True
    context_injection = True
    output_file = "outputs/ask_me_response_{timestamp}.json"
    guardrails = {
        "retry_on_fail": 2,
        "fallback_response": {
            "answer": "Sorry, I couldn't generate a confident answer. Please rephrase the question.",
            "source_context": None,
            "follow_up_question": "Can you ask the question differently?",
            "confidence_score": 0.0,
            "suggested_agents": ["BhāṣāGuru"]
        }
    }
    metadata = {
        "agent": "AskMeAgent",
        "audience": "Teachers and Students",
        "grade_range": "1-10 and UG",
        "dialect_support": True,
        "uses_contextual_memory": True,
        "downstream_support": ["VoiceAgent", "CoursePlannerAgent", "QuizAgent"],
    }

    async def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Async run method to process the question and return structured answer.
        
        Args:
            inputs (dict): Should contain keys like 'question', 'grade_level', 'dialect', etc.
        
        Returns:
            dict: Parsed response adhering to AskMeResponseSchema.
        """
        question = inputs.get("question")
        grade_level = inputs.get("grade_level", "medium")
        dialect = inputs.get("dialect", "default")
        prior_context = inputs.get("prior_context", "")

        # Placeholder: Replace this with your actual LLM call and processing
        try:
            # For example, asynchronously call Gemini LLM API or another service here
            # Simulate async call delay
            await asyncio.sleep(0.1)

            # Dummy generated response (replace with real generation)
            answer = f"Simulated answer for question: {question}"
            source_context = prior_context or "No prior context found."
            follow_up_question = "Would you like more details on this topic?"
            confidence_score = 0.95

            # Validate and create output schema instance
            response = AskMeResponseSchema(
                answer=answer,
                source_context=source_context,
                follow_up_question=follow_up_question,
                confidence_score=confidence_score,
                suggested_agents=["CoursePlannerAgent", "BhāṣāGuru"]
            )
            return response.dict()

        except Exception as e:
            # Handle errors and fallback
            fallback = self.guardrails.get("fallback_response")
            fallback["answer"] += f" Error details: {str(e)}"
            return fallback

# Create an instance of the task for agent usage
ask_question_task = AskMeTask()
