# tools/ask_me_tool.py

import os
import json
from typing import Dict, Optional
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

class AskMeTool:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.4,
            convert_system_message_to_human=True
        )

        self.prompt_template = PromptTemplate.from_template("""
You are a doubt-solving AI designed for Indian education systems across different grades and dialects.

Context:
---------
{context}

Student/Teacher Question:
-------------------------
{question}

Instructions:
-------------
1. Answer based only on the provided context. Avoid hallucinating.
2. Use regional language tone if dialect is specified.
3. Generate a possible follow-up question to extend learning.
4. Output in valid JSON with keys:
   - answer
   - source_context
   - follow_up_question
   - suggested_agents
   - confidence_score (0.0–1.0)

Respond only in JSON format.
""")

    def run(self, inputs: Dict) -> Dict:
        question = inputs.get("question", "What is transpiration?")
        context = inputs.get("context", "Plants lose water through small pores called stomata.")
        
        prompt = self.prompt_template.format(question=question, context=context)
        result = self.llm.invoke(prompt)

        try:
            response_json = json.loads(result.content)
            return response_json
        except json.JSONDecodeError:
            return {
                "error": "Failed to parse response. LLM did not return valid JSON.",
                "raw_response": result.content
            }

    @retry_on_failure()
    def run(self, inputs: Dict) -> Dict:
        question = inputs.get("question", "What is photosynthesis?")
        context = inputs.get("context", "Photosynthesis is the process by which plants make food.")

        logger.info(f"Answering question: {question}")
        prompt = self.prompt_template.format(question=question, context=context)
        result = self.llm.invoke(prompt)

        try:
            return json.loads(result.content)
        except json.JSONDecodeError:
            logger.error("Invalid JSON received for AskMeTool")
            return {"error": "AskMeTool failed. Output was not valid JSON.", "raw_response": result.content}

