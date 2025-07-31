from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from firebase_admin import auth
from firestore.firebase_config import db
from datetime import datetime

router = APIRouter()

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str
    role: str
    grade: int = None
    student_id: str = None

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(request: RegisterRequest):
    try:
        user = auth.create_user(email=request.email, password=request.password)

        user_data = {
            "email": request.email,
            "name": request.name,
            "role": request.role,
            "created_at": datetime.utcnow(),
        }

        if request.role == "student":
            user_data["grade"] = request.grade
            user_data["student_id"] = request.student_id
            db.collection("students").document(user.uid).set(user_data)
        else:
            db.collection("users").document(user.uid).set(user_data)

        return {"message": "User registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Registration failed: {e}")

@router.post("/login")
def login(request: LoginRequest):
    # Firebase Admin SDK doesn't support password login. Use Firebase Auth on frontend.
    raise HTTPException(status_code=501, detail="Login via password is not supported on backend. Use Firebase client SDK.")
