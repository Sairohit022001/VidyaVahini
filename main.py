from dotenv import load_dotenv
load_dotenv()
import os
from dotenv import load_dotenv
load_dotenv()  # This loads variables from .env into environment

import sys
import signal
import time
import asyncio
import logging
from fastapi import FastAPI, Request, HTTPException, Depends, status, APIRouter
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, validator, field_validator # Import field_validator
from typing import Optional, Dict, AsyncIterator # Import AsyncIterator
from functools import wraps
import structlog
import traceback
from contextlib import asynccontextmanager # Import asynccontextmanager

 
from agents.lesson_planner_agent import lesson_planner_agent
from agents.story_teller_agent import story_teller_agent
from agents.quiz_agent import quiz_agent
from agents.sync_agent import sync_agent
from agents.course_planner_agent import course_planner_agent
from agents.ask_me_agent import ask_me_agent
from agents.teacher_dashboard_agent import teacher_dashboard_agent
from agents.voice_tutor_agent import voice_tutor_agent
from agents.student_level_analytics_agent import student_level_analytics_agent
from agents.visual_agent import visual_agent
from agents.multimodal_research_agent import multimodal_research_agent
from agents.predictive_analytics_agent import predictive_analytics_agent
from agents.gamification_agent import gamification_agent
from agents.content_creator_agent import content_creator_agent

from crewflows import Crew
from crewflows.memory.local_memory_handler import LocalMemoryHandler
from llms.llm_config import custom_llm_config



credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if credentials_path:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
else:
    raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS is not set in environment variables")


google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    raise ValueError("GOOGLE_API_KEY is not set in environment variables!")


from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(google_api_key=google_api_key, model="models/gemini-2.5-pro") # Remove convert_system_message_to_human

# FastAPI Lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info("FastAPI lifespan startup event triggered. Initializing resources...")
    # Add any startup code here
    yield
    # Shutdown logic
    logger.info("FastAPI lifespan shutdown event triggered. Cleaning up resources...")
    # Add any shutdown code here
    await asyncio.sleep(0.1)

# Initialize FastAPI app once here
app = FastAPI(
    title="VIDYAVAHINI",
    description="Empowering teachers in multi-grade classrooms",
    version="1.0.0",
    lifespan=lifespan # Pass the decorated lifespan function here
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging setup
logging.basicConfig(
    format="%(message)s",
    stream=sys.stdout,
    level=logging.INFO,
)
logger = structlog.get_logger("vidyavahini_main")

MAX_PROMPT_LENGTH = 2000
API_KEY = os.getenv("VIDYAVAHINI_API_KEY")
if not API_KEY:
    logger.error("API key not set in environment variable VIDYAVAHINI_API_KEY")
    sys.exit(1)

# Helper functions & global variables
def get_client_ip(request: Request) -> str:
    return request.client.host if request.client else "unknown"

RATE_LIMIT = 20
RATE_LIMIT_INTERVAL = 60
client_requests = {}

def rate_limiter(client_ip: str) -> bool:
    current_time = time.time()
    window_start = current_time - RATE_LIMIT_INTERVAL
    if client_ip not in client_requests:
        client_requests[client_ip] = []
    client_requests[client_ip] = [t for t in client_requests[client_ip] if t > window_start]
    if len(client_requests[client_ip]) >= RATE_LIMIT:
        return False
    client_requests[client_ip].append(current_time)
    return True

async def verify_api_key(request: Request):
    api_key = request.headers.get("x-api-key")
    client_ip = get_client_ip(request)
    if api_key != API_KEY:
        logger.warning("Unauthorized access attempt", client_ip=client_ip)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")
    return True

# Memory handler and Crew initialization
global_memory = LocalMemoryHandler(
    session_id="vidyavahini_main_session",
    file_path="memory/vidyavahini_main_memory.json"
)

vidyavahini_crew = Crew(
    agents=[
        lesson_planner_agent,
        story_teller_agent,
        quiz_agent,
        sync_agent,
        course_planner_agent,
        ask_me_agent,
        teacher_dashboard_agent,
        voice_tutor_agent,
        student_level_analytics_agent,
        content_creator_agent,
        # gamification_agent, # Comment out GamificationAgent here
        multimodal_research_agent,
        predictive_analytics_agent,
        visual_agent,
    ],
    verbose=True,
    memory=True,
    memory_handler=global_memory,
    llm_config=custom_llm_config,
    process_config={
        "executor_type": "kirchhoff-async",
        "auto_delegate": True,
    },
    crew_description="""
    VidyaVāhinī is a next-gen AI-powered education platform driven by an agentic crew that supports teachers and students
    in a multilingual, multimodal, and offline-first environment.
    This crew generates explainable lessons, stories, quizzes, visuals, dialect-specific translations, and student-level analytics to revolutionize digital learning.
    """,
)

# Request and response models
class CrewRequest(BaseModel):
    prompt: str = Field(..., max_length=MAX_PROMPT_LENGTH, description="User prompt for AI Crew")
    context: Optional[Dict] = Field(default_factory=dict)

    # Use field_validator for Pydantic V2
    @field_validator("prompt")
    @classmethod
    def no_empty_prompt(cls, v):
        if not v.strip():
            raise ValueError("Prompt cannot be empty or whitespace")
        return v

class CrewResponse(BaseModel):
    result: Dict
    message: Optional[str] = "Success"

# Rate limit decorator
def rate_limit_endpoint(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        client_ip = get_client_ip(request)
        if not rate_limiter(client_ip):
            logger.warning("Rate limit exceeded", client_ip=client_ip)
            raise HTTPException(status_code=429, detail="Too Many Requests")
        return await func(request, *args, **kwargs)
    return wrapper

# Routes
@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "ok"}

@app.post("/api/run", response_model=CrewResponse, dependencies=[Depends(verify_api_key)])
@rate_limit_endpoint
async def run_crew(request: Request, crew_request: CrewRequest):
    """
    Run the entire VidyaVāhinī agent crew on the given prompt and context.
    """
    client_ip = get_client_ip(request)
    logger.info("Received /api/run request", client_ip=client_ip, prompt=crew_request.prompt[:50])
    try:
        result = await asyncio.wait_for(
            vidyavahini_crew.run(inputs={"prompt": "what is photosynthesis", "dialect": "Telangana"}),
            timeout=60.0
        )
        logger.info("Crew run completed successfully", client_ip=client_ip)
        return CrewResponse(result=result)
    except asyncio.TimeoutError:
        logger.error("Crew run timed out", client_ip=client_ip)
        raise HTTPException(status_code=504, detail="Crew processing timed out")
    except Exception as e:
        error_trace = traceback.format_exc()
        logger.error("Crew execution error", client_ip=client_ip, error=str(e), trace=error_trace)
        raise HTTPException(status_code=500, detail="Internal server error")

# Helper function to run a single agent
async def run_single_agent(agent, prompt: str, context: Optional[Dict]):
    try:
        result = await asyncio.wait_for(
            agent.run(prompt=prompt, context=context or {}),
            timeout=60.0
        )
        return result
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail=f"{agent.name} processing timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{agent.name} internal error: {str(e)}")

# Dictionary mapping endpoint suffixes to agents
agent_endpoints = {
    "lesson_planner": lesson_planner_agent,
    "story_teller": story_teller_agent,
    "quiz": quiz_agent,
    "sync": sync_agent,
    "course_planner": course_planner_agent,
    "ask_me": ask_me_agent,
    "teacher_dashboard": teacher_dashboard_agent,
    "voice_tutor": voice_tutor_agent,
    "student_level_analytics": student_level_analytics_agent,
    "content_creator": content_creator_agent,
    # "gamification": gamification_agent, # Comment out GamificationAgent here as well for consistency
    "multimodal_research": multimodal_research_agent,
    "predictive_analytics": predictive_analytics_agent,
    "visual": visual_agent,
}

api_router = APIRouter()

# Dynamically add one endpoint per agent
def create_agent_endpoint(agent, endpoint_name):
    @rate_limit_endpoint
    async def endpoint_func(request: Request, crew_request: CrewRequest):
        client_ip = get_client_ip(request)
        logger.info(f"Received /api/{endpoint_name} request", client_ip=client_ip, prompt=crew_request.prompt[:50])
        result = await run_single_agent(agent, crew_request.prompt, crew_request.context)
        logger.info(f"Agent {agent.name} run completed successfully", client_ip=client_ip)
        return CrewResponse(result=result)
    return endpoint_func

for endpoint_name, agent in agent_endpoints.items():
    api_router.post(
        f"/api/{endpoint_name}",
        response_model=CrewResponse,
        dependencies=[Depends(verify_api_key)],
        tags=["Agents"],
        summary=f"Run {agent.name} agent"
    )(create_agent_endpoint(agent, endpoint_name))

app.include_router(api_router)

# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    client_ip = get_client_ip(request)
    logger.warning("Validation error", client_ip=client_ip, errors=exc.errors())
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    client_ip = get_client_ip(request)
    logger.warning("HTTP error", client_ip=client_ip, status_code=exc.status_code, detail=exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    client_ip = get_client_ip(request)
    logger.error("Unhandled error", client_ip=client_ip, error=str(exc), exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

# Graceful shutdown (keep signal handlers for external signals)
shutdown_event = asyncio.Event()

def handle_shutdown(signum, frame):
    global shutdown_event # Declare shutdown_event as global
    logger.info(f"Shutdown signal received: {signum}. Triggering FastAPI shutdown...")
    shutdown_event.set()
    # You might want to trigger FastAPI's shutdown programmatically here
    # depending on your uvicorn setup. Sending a signal might be enough.

signal.signal(signal.SIGINT, handle_shutdown)
signal.signal(signal.SIGTERM, handle_shutdown)

# CLI runner for manual testing
async def main():
    test_prompt = "Prepare a summary lesson plan on photosynthesis for Grade 7."
    logger.info("Starting VidyaVāhinī Crew CLI run...")
    try:
        # Example of providing more complete inputs for a lesson planning scenario
        inputs = {
            "topic": "Photosynthesis",
            "level": "7", # Use "level" instead of "grade" for consistency with LessonPlannerAgent
            "dialect": "Telangana",
            "prompt": "Explain photosynthesis for grade 7 students in Telangana dialect.", # Add prompt here
            # Add other potential inputs needed by agents in the crew
            # based on their add_input declarations and task requirements
            # Example for StoryTellerAgent (requires lesson_plan_json):
            "lesson_plan_json": {
                "title": "The Magical Process of Photosynthesis",
                "sections": [
                    {"heading": "Introduction", "content": "Brief intro to photosynthesis."},
                    {"heading": "What is Needed?", "content": "Sunlight, water, CO2."},
                    {"heading": "The Process", "content": "How plants make food."},
                    {"heading": "Importance", "content": "Why photosynthesis is important."}
                ]
            },
            # Example for QuizAgent (requires lesson_plan_json, story_body, or audio_data):
            "story_body": "A short story about a plant making food.",
            # Example for TeacherDashboardAgent (requires quiz_data, student_levels, predictive_data):
            "quiz_data": {"total_students": 10, "completed_quizzes": 8, "results": []}, # Example structure, provide empty list
            "student_levels": {}, # Example structure, provide empty dict
            "predictive_data": {}, # Example structure, provide empty dict
            # Example for StudentLevelAnalyticsAgent (requires student_id, quiz_results, interaction_data):
            "student_id": "student123",
            "quiz_results": [], # Example structure, provide empty list
            "interaction_data": {}, # Example structure, provide empty dict
            # Example for ContentCreatorAgent (requires lesson_plan_json, story_body, visual_prompts):
            "visual_prompts": [], # Example structure, provide empty list
            # Example for MultimodalResearchAgent (requires topic, grade, context_from_doc):
            # topic, grade, dialect are already included above
            "context_from_doc": {}, # Example structure, provide empty dict
            # Example for PredictiveAnalyticsAgent (requires quiz_results):
            # quiz_results is already included above
            # Example for VisualAgent (requires lesson_plan_json, story_text, dialect):
            "story_text": "A story related to photosynthesis."

        }

        result = await vidyavahini_crew.run(inputs=inputs)
        logger.info("CLI run result:") # Close the string here
        logger.info(f"{result}") # Print the result on a new line
    except Exception as e:
        logger.error(f"Error running crew in CLI: {e}")

if __name__ == "__main__":
    asyncio.run(main())
