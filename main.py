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
from contextlib import asynccontextmanager 

 
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
from routes.firestore_routes import router as firestore_router



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


from fastapi.openapi.utils import get_openapi
from fastapi.security.api_key import APIKeyHeader
from fastapi import Security

# Define headers as security schemes
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)
user_role_header = APIKeyHeader(name="x-user-role", auto_error=False)
user_level_header = APIKeyHeader(name="x-user-level", auto_error=False)

# Custom OpenAPI with security headers shown
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="VIDYAVAHINI",
        version="1.0.0",
        description="Empowering teachers in multi-grade classrooms",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "x-api-key": {"type": "apiKey", "name": "x-api-key", "in": "header"},
        "x-user-role": {"type": "apiKey", "name": "x-user-role", "in": "header"},
        "x-user-level": {"type": "apiKey", "name": "x-user-level", "in": "header"},
    }
    openapi_schema["security"] = [
        {"x-api-key": [], "x-user-role": [], "x-user-level": []}
    ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# ✅ Include Firestore agent operation routes
app.include_router(
    firestore_router,
    prefix="/firestore",         # All endpoints will be under /firestore
    tags=["Firestore Operations"]
)

from fastapi import APIRouter, Header
from pydantic import BaseModel

class UserRegister(BaseModel):
    email: str
    password: str
    role: str  # "student" or "teacher"
    user_data: dict

class ClassCreate(BaseModel):
    class_id: str
    class_data: dict
    teacher_uid: str
    subject: str

class AddStudent(BaseModel):
    class_id: str
    student_id: str

class QuizPost(BaseModel):
    teacher_uid: str
    class_id: str
    subject: str
    quiz_data: dict

@app.post("/register")
def register(user: UserRegister):
    try:
        user_id = register_user(user.email, user.password, user.role, user.user_data)
        return {"message": "User registered", "uid": user_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/class/create")
def create_class_endpoint(cls: ClassCreate):
    try:
        create_class(cls.class_id, cls.class_data, cls.teacher_uid, cls.subject)
        return {"message": "Class created"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/class/add-student")
def add_student(cls: AddStudent):
    try:
        add_student_to_class(cls.class_id, cls.student_id)
        return {"message": "Student added to class"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/quiz/post")
def post_quiz(q: QuizPost):
    try:
        post_quiz_result(q.teacher_uid, q.class_id, q.subject, q.quiz_data)
        return {"message": "Quiz posted to class"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class CoursePlannerInput(BaseModel):
    current_topic: str
    quiz_score: int




# ✅ Optional: Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to VidyaVāhinī Agentic Backend 🚀"}

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

# --- New function: Determine agents accessible based on user role and level ---
def get_allowed_agents(user_role: str, user_level: Optional[int]):
    """
    Returns a set of agents allowed for the user based on role and level.
    - Students with level <= 10 get limited basic agents.
    - Students with level > 10 get mid-level agents.
    - Teachers get all agents.
    """
    # Define sets of agent names for each category
    basic_agents = {"voice_tutor_agent", "story_teller_agent", "quiz_agent"}
    mid_agents = {"ask_me_agent", "lesson_planner_agent", "course_planner_agent", "sync_agent"}
    teacher_agents = {
        "lesson_planner_agent",
        "story_teller_agent",
        "quiz_agent",
        "sync_agent",
        "course_planner_agent",
        "ask_me_agent",
        "teacher_dashboard_agent",
        "voice_tutor_agent",
        "student_level_analytics_agent",
        "content_creator_agent",
        "multimodal_research_agent",
        "predictive_analytics_agent",
        "visual_agent",
        # "gamification_agent", 
    }

    


@app.post("/manage-content")
async def manage_content(request: Request):
    headers = request.headers
    user_role = headers.get("x-user-role", "student").lower()

    if user_role != "teacher":
        return JSONResponse(content={"error": "Only teachers can manage content"}, status_code=403)

    body = await request.json()
    action = body.get("action")  # Expected: 'save', 'edit', 'publish', 'draft'
    content = body.get("content")
    content_type = body.get("type", "unknown")
    topic = body.get("topic", "unknown")

    if not content or not action:
        return JSONResponse(content={"error": "Content and action are required"}, status_code=400)

    # Simulated logic for storing different types of updates (extendable to Firestore later)
    print(f"[ACTION: {action.upper()} BY TEACHER]")
    print(f"Type: {content_type}")
    print(f"Topic: {topic}")
    print("Content:")
    print(content)

    return {
        "status": "success",
        "message": f"Content for topic '{topic}' {action.lower()}ed successfully."
    }


# Helper to map agent instance names to their string keys used above
agent_instance_to_name = {
    lesson_planner_agent: "lesson_planner_agent",
    story_teller_agent: "story_teller_agent",
    quiz_agent: "quiz_agent",
    sync_agent: "sync_agent",
    course_planner_agent: "course_planner_agent",
    ask_me_agent: "ask_me_agent",
    teacher_dashboard_agent: "teacher_dashboard_agent",
    voice_tutor_agent: "voice_tutor_agent",
    student_level_analytics_agent: "student_level_analytics_agent",
    content_creator_agent: "content_creator_agent",
    multimodal_research_agent: "multimodal_research_agent",
    predictive_analytics_agent: "predictive_analytics_agent",
    visual_agent: "visual_agent",
    # gamification_agent is commented out
}

# Dictionary mapping endpoint suffixes to agents (same as before)
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
    # "gamification": gamification_agent, # Commented out GamificationAgent
    "multimodal_research": multimodal_research_agent,
    "predictive_analytics": predictive_analytics_agent,
    "visual": visual_agent,
}

# Helper function to run a single agent
async def run_single_agent(agent, prompt: str, context: Optional[Dict]):
    try:
        result = await asyncio.wait_for(
            agent.run(prompt=prompt, context=context or {}),
            timeout=60.0
        )
        if result is None or not isinstance(result, dict):
            logger.error(f"Agent {agent.name} returned invalid result: {result}")
            raise HTTPException(status_code=500, detail=f"Agent {agent.name} returned no valid result")
        return result
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail=f"{agent.name} processing timed out")
    except Exception as e:
        logger.error(f"Agent {agent.name} internal error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"{agent.name} internal error: {str(e)}")


api_router = APIRouter()

# Dynamically add one endpoint per agent with role-based access control
def create_agent_endpoint(agent, endpoint_name):
    @rate_limit_endpoint
    async def endpoint_func(request: Request, crew_request: CrewRequest):
        client_ip = get_client_ip(request)
        logger.info(f"Received /api/{endpoint_name} request", client_ip=client_ip, prompt=crew_request.prompt[:50])

        # existing user role checks ...
        
        result = await run_single_agent(agent, crew_request.prompt, crew_request.context)

        logger.info(f"Agent returned result: {result}")

        if result is None:
            logger.error(f"Agent {agent.name} returned None instead of dict")
            raise HTTPException(status_code=500, detail=f"Agent {agent.name} returned no result")

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
    User role/level filtering applied: only runs allowed agents
    """
    client_ip = get_client_ip(request)
    logger.info("Received /api/run request", client_ip=client_ip, prompt=crew_request.prompt[:50])

    # Get user role and level from headers
    user_role = request.headers.get("x-user-role", "").lower()
    user_level_str = request.headers.get("x-user-level")
    user_level = None
    if user_level_str:
        try:
            user_level = int(user_level_str)
        except ValueError:
            logger.warning(f"Invalid x-user-level header value: {user_level_str}")

    allowed_agents_names = get_allowed_agents(user_role, user_level)

    # Filter the crew's agents for allowed ones only
    filtered_agents = [agent for agent in vidyavahini_crew.agents if agent_instance_to_name.get(agent) in allowed_agents_names]

    if not filtered_agents:
        logger.warning(f"No agents allowed for user_role={user_role}, user_level={user_level}", client_ip=client_ip)
        raise HTTPException(status_code=403, detail="No agents available for your user role/level")

    # Extract topic from prompt (simple extraction)
    prompt_lower = crew_request.prompt.lower()
    topic = "plants"  # Default fallback
    grade = "5"       # Default fallback
    
    # Simple topic extraction from prompt
    if "math" in prompt_lower or "mathematics" in prompt_lower:
        topic = "mathematics"
    elif "science" in prompt_lower:
        topic = "science"
    elif "plant" in prompt_lower:
        topic = "plants"
    elif "animal" in prompt_lower:
        topic = "animals"
    elif "history" in prompt_lower:
        topic = "history"
    
    # Extract grade from prompt
    import re
    grade_match = re.search(r'grade (\d+)', prompt_lower)
    if grade_match:
        grade = grade_match.group(1)

    # Create comprehensive inputs for all agents
    comprehensive_inputs = {
        "prompt": crew_request.prompt,
        
        # For LessonPlannerAgent
        "topic": topic,
        "level": grade,  # LessonPlannerAgent uses "level" not "grade"
        "dialect": "English",  # Default to English for hackathon
        
        # Sample lesson plan structure for dependent agents
        "lesson_plan_json": {
            "title": f"Introduction to {topic.title()}",
            "grade": grade,
            "subject": topic,
            "sections": [
                {
                    "heading": "Introduction",
                    "content": f"Welcome to learning about {topic}!",
                    "duration": "10 minutes"
                },
                {
                    "heading": "Main Concepts",
                    "content": f"Key concepts about {topic}...",
                    "duration": "20 minutes"
                },
                {
                    "heading": "Activities",
                    "content": f"Fun activities related to {topic}...",
                    "duration": "15 minutes"
                },
                {
                    "heading": "Summary",
                    "content": f"What we learned about {topic}.",
                    "duration": "5 minutes"
                }
            ]
        },
        
        # For StoryTellerAgent and QuizAgent
        "story_body": f"Once upon a time, there was a curious student who wanted to learn about {topic}...",
        
        # For TeacherDashboardAgent
        "quiz_data": {
            "total_students": 25,
            "completed_quizzes": 20,
            "results": [
                {"student_id": f"student_{i}", "score": 85 + (i % 15)} 
                for i in range(1, 21)
            ]
        },
        "student_levels": {f"student_{i}": 7 + (i % 4) for i in range(1, 26)},
        "predictive_data": {
            "engagement_scores": [0.8, 0.7, 0.9, 0.6, 0.8],
            "completion_rates": [0.9, 0.8, 0.95, 0.7, 0.85]
        },
        
        # For StudentLevelAnalyticsAgent
        "student_id": "demo_student_001",
        "quiz_results": [
            {"quiz_id": "q1", "score": 85, "topic": topic},
            {"quiz_id": "q2", "score": 78, "topic": topic}
        ],
        "interaction_data": {
            "time_spent": 45,
            "questions_asked": 3,
            "help_requests": 1
        },
        
        # For ContentCreatorAgent
        "visual_prompts": [
            f"Illustration of {topic} for grade {grade}",
            f"Diagram showing {topic} concepts",
            f"Interactive {topic} activity"
        ],
        
        # For MultimodalResearchAgent
        "context_from_doc": {
            "source": "educational_standards",
            "grade_level": grade,
            "subject": topic
        },
        
        # For VisualAgent
        "story_text": f"Educational story about {topic} for grade {grade} students.",
        
        # Add any additional context from the request
        **(crew_request.context or {})
    }

    # Create filtered crew with proper configuration
    filtered_crew = Crew(
        agents=filtered_agents,
        verbose=True,
        memory=True,
        memory_handler=global_memory,
        llm_config=custom_llm_config,
        process_config={
            "executor_type": "kirchhoff-async",
            "auto_delegate": True,
        },
        crew_description=f"""
        VidyaVāhinī filtered crew for {user_role} (level {user_level}).
        Processing educational content about {topic} for grade {grade}.
        """,
    )

    try:
        result = await asyncio.wait_for(
            filtered_crew.run(inputs=comprehensive_inputs),
            timeout=120.0  # Increased timeout for hackathon
        )
        logger.info("Crew run completed successfully", client_ip=client_ip)
        return CrewResponse(result=result)
    except asyncio.TimeoutError:
        logger.error("Crew run timed out", client_ip=client_ip)
        raise HTTPException(status_code=504, detail="Crew processing timed out")
    except Exception as e:
        error_trace = traceback.format_exc()
        logger.error("Crew execution error", client_ip=client_ip, error=str(e), trace=error_trace)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

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
    global shutdown_event 
    logger.info(f"Shutdown signal received: {signum}. Triggering FastAPI shutdown...")
    shutdown_event.set()
    
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
        logger.info("CLI run result:") 
        logger.info(f"{result}") 
    except Exception as e:
        logger.error(f"Error running crew in CLI: {e}")
        return result

if __name__ == "__main__":
    asyncio.run(main())
