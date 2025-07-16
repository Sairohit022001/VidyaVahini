from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
import json
import logging

from tools.utils.retry_handler import retry_with_backoff
from tools.utils.logger import get_logger
from tools.utils.prompt_loader import load_prompt
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

logger = get_logger("AskMeTool")

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

class AskMeTool:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.7,
            convert_system_message_to_human=True
        )
        self.prompt_template = PromptTemplate.from_template(load_prompt("ask_me.txt"))

    @retry_with_backoff()
    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        question = inputs.get("question", "")
        context = inputs.get("context", "")
        dialect = inputs.get("dialect", "Telangana Telugu")

        prompt = self.prompt_template.format(
            question=question,
            context=context,
            dialect=dialect
        )

        result = self.llm.invoke(prompt)

        try:
            response_text = str(result.content).strip()
            logger.info("✅ AskMe response generated")
            return response_text if isinstance(response_text, dict) else AskMeResponseSchema.parse_raw(response_text).dict()
        except json.JSONDecodeError:
            logger.error("❌ JSON decoding failed in AskMeTool. Raw response:\n%s", result.content)
            return {
                "error": "Invalid JSON response from LLM.",
                "raw_response": result.content
            }
        except Exception as e:
            logger.exception("🚨 Unexpected error in AskMeTool")
            return {
                "error": "Unexpected error during AskMe response generation.",
                "details": str(e)
            }
