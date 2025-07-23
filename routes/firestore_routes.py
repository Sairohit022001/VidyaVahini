from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from firestore import firestore_utils as fs

router = APIRouter()

# ----------- Shared Schemas -------------
class UserData(BaseModel):
    user_id: str
    name: str
    email: str
    role: str

class LessonPlan(BaseModel):
    user_id: str
    title: str
    summary: str

class StoryData(BaseModel):
    user_id: str
    title: str
    content: str

class CoursePlan(BaseModel):
    user_id: str
    course_title: str
    objectives: list[str]

class QuizResult(BaseModel):
    user_id: str
    score: float
    questions: list[dict]

class VoiceSession(BaseModel):
    user_id: str
    transcript: str
    duration_sec: int

class VisualAsset(BaseModel):
    user_id: str
    description: str
    image_url: str

class QAData(BaseModel):
    user_id: str
    question: str
    answer: str

class SyncEvent(BaseModel):
    user_id: str
    event_type: str
    details: dict

class DashboardData(BaseModel):
    user_id: str
    metrics: dict

class GeneratedContent(BaseModel):
    user_id: str
    content_type: str
    data: str

class GameResult(BaseModel):
    user_id: str
    game_name: str
    score: int

class Prediction(BaseModel):
    user_id: str
    input_data: dict
    prediction: str

class MultimodalResearch(BaseModel):
    user_id: str
    summary: str
    visuals: list[str]

class StudentAnalytics(BaseModel):
    user_id: str
    activity_type: str
    engagement_score: float

# ----------- Routes -------------

@router.post("/create_user")
def create_user(user: UserData):
    fs.create_user_profile(user.user_id, user.dict())
    return {"status": "User created"}

@router.get("/get_user/{user_id}")
def get_user(user_id: str):
    profile = fs.get_user_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    return profile

@router.post("/save_lesson")
def save_lesson(data: LessonPlan):
    fs.create_lesson_plan(data.user_id, data.dict())
    return {"status": "Lesson saved"}

@router.get("/get_lessons/{user_id}")
def get_lessons(user_id: str):
    return fs.get_lesson_plans(user_id)

@router.post("/save_story")
def save_story(data: StoryData):
    fs.save_story(data.user_id, data.dict())
    return {"status": "Story saved"}

@router.get("/get_stories/{user_id}")
def get_stories(user_id: str):
    return fs.get_stories(user_id)

@router.post("/save_course")
def save_course(data: CoursePlan):
    fs.save_course_plan(data.user_id, data.dict())
    return {"status": "Course plan saved"}

@router.post("/save_quiz")
def save_quiz(data: QuizResult):
    fs.save_quiz_result(data.user_id, data.dict())
    return {"status": "Quiz result saved"}

@router.get("/get_quizzes/{user_id}")
def get_quizzes(user_id: str):
    return fs.get_quiz_results(user_id)

@router.post("/log_voice_session")
def log_voice(data: VoiceSession):
    fs.log_voice_session(data.user_id, data.dict())
    return {"status": "Voice session logged"}

@router.post("/save_visual")
def save_visual(data: VisualAsset):
    fs.save_visual_asset(data.user_id, data.dict())
    return {"status": "Visual asset saved"}

@router.post("/ask_me")
def log_qa(data: QAData):
    fs.log_qa(data.user_id, data.question, data.answer)
    return {"status": "Q&A logged"}

@router.post("/log_sync")
def log_sync(data: SyncEvent):
    fs.log_sync_event(data.user_id, data.dict())
    return {"status": "Sync event logged"}

@router.post("/dashboard_data")
def save_dashboard(data: DashboardData):
    fs.record_teacher_metrics(data.user_id, data.dict())
    return {"status": "Dashboard data saved"}

@router.post("/save_content")
def save_generated(data: GeneratedContent):
    fs.save_generated_content(data.user_id, data.dict())
    return {"status": "Generated content saved"}

@router.post("/save_game_result")
def save_game(data: GameResult):
    fs.save_game_result(data.user_id, data.dict())
    return {"status": "Game result saved"}

@router.post("/save_prediction")
def save_prediction(data: Prediction):
    fs.save_prediction(data.user_id, data.dict())
    return {"status": "Prediction saved"}

@router.post("/log_research")
def save_research(data: MultimodalResearch):
    fs.log_multimodal_result(data.user_id, data.dict())
    return {"status": "Multimodal research saved"}

@router.post("/student_analytics")
def save_student_analytics(data: StudentAnalytics):
    fs.log_student_analytics(data.user_id, data.dict())
    return {"status": "Student analytics logged"}
