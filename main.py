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


from crewai import Crew
from crewai.memory.local_memory_handler import LocalMemoryHandler
from llms.llm_config import custom_llm_config

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
        gamification_agent,
        multimodal_research_agent,
        predictive_analytics_agent,
        visual_agent
    ],
    verbose=True,
    memory=True,
    memory_handler=global_memory,
    llm_config={
        "model": "gemini-pro",
        "temperature": 0.65,
        "top_p": 0.9,
        "presence_penalty": 0.3,
    },
    process_config={
        "executor_type": "kirchhoff-async",
        "auto_delegate": True,
    },
    crew_description="""
VidyaVāhinī is a next-gen AI-powered education platform driven by an agentic crew that supports teachers and students in a multilingual, multimodal, and offline-first environment.
This crew generates explainable lessons, stories, quizzes, visuals, dialect-specific translations, and student-level analytics to revolutionize digital learning.
"""
)