from fastapi import APIRouter, Query
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sarvam_client import sarvam_translate

router = APIRouter()

@router.get("/translate")
def translate(text: str = Query(...), source: str = Query("en"), target: str = Query("te-IN")):
    result = sarvam_translate(text, source, target)
    return result
