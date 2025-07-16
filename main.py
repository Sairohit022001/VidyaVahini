import asyncio
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from typing import Optional
from fastapi import status
logging.basicConfig(level=logging.INFO)

from agents.lesson_planner_agent import lesson_planner_agent
from agents.story_teller_agent import story_teller_agent
from agents.quiz_agent import quiz_agent
from agents.sync_agent import sync_agent
from agents.course_planner_agent import course_planner_agent
from agents.ask_me_agent import ask_me_agent
from agents.teacher_dashboard_agent import teacher_dashboard_agent
from agents.voice_tutor_agent import voice_tutor_agent
from agents.student_level_analytics_agent import student_analytics_agent 
from agents.visual_agent import visual_agent
from agents.multimodal_research_agent import multimodal_research_agent
from agents.predictive_analytics_agent import predictive_analytics_agent
from agents.gamification_agent import gamification_agent
from agents.content_creator_agent import content_creator_agent