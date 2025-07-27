from fastapi import APIRouter, Query
from sarvam_client import sarvam_translate

router = APIRouter()

@router.get("/translate")
def translate(text: str = Query(...), source: str = Query("en"), target: str = Query("te-IN")):
    result = sarvam_translate(text, source, target)
    return result
