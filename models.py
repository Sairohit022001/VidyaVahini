from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, EmailStr, constr
from database import Base

# SQLAlchemy ORM User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)  # 'student' or 'teacher'
    grade = Column(Integer, nullable=True)
    student_id = Column(String, nullable=True)

# Pydantic schemas for requests/responses

class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
    name: str
    role: str
    grade: int | None = None
    student_id: str | None = None

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: str
    grade: int | None = None
    student_id: str | None = None

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
