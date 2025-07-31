from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import User, UserCreate, UserLogin, Token, UserResponse
from database import SessionLocal, engine, Base
from auth import hash_password, verify_password, create_access_token

Base.metadata.create_all(bind=engine)

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserResponse)
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    # Check if email exists
    existing_user = db.query(User).filter(User.email == user_create.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create user
    hashed_pw = hash_password(user_create.password)
    db_user = User(
        email=user_create.email,
        hashed_password=hashed_pw,
        name=user_create.name,
        role=user_create.role,
        grade=user_create.grade,
        student_id=user_create.student_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@router.post("/login", response_model=Token)
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_login.email).first()
    if not user or not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}
