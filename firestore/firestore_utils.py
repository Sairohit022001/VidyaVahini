from firebase_admin import firestore
from firestore.firebase_config import db
# use db here...


# # ------------------------------------------
# # User Profile Firestore Operations
# # ------------------------------------------

# def create_user_profile(user_id: str, user_data: dict):
#     """
#     Create a new user profile document in Firestore.
    
#     Args:
#         user_id (str): Unique user identifier (e.g., Firebase Auth UID)
#         user_data (dict): Dictionary of user profile data (name, email, role, etc.)
#     """
#     user_ref = db.collection("users").document(user_id)
#     user_ref.set({
#         **user_data,
#         "created_at": firestore.SERVER_TIMESTAMP
#     })
#     print(f"[Firestore] Created user profile for user_id: {user_id}")

# def get_user_profile(user_id: str) -> dict | None:
#     """
#     Retrieve a user profile document by user_id.
    
#     Args:
#         user_id (str): Unique user identifier
        
#     Returns:
#         dict or None: User profile data if exists, else None
#     """
#     user_ref = db.collection("users").document(user_id)
#     doc = user_ref.get()
#     if doc.exists:
#         print(f"[Firestore] Retrieved user profile for user_id: {user_id}")
#         return doc.to_dict()
#     else:
#         print(f"[Firestore] No user profile found for user_id: {user_id}")
#         return None

# def update_user_profile(user_id: str, updates: dict):
#     """
#     Update fields in an existing user profile document.
    
#     Args:
#         user_id (str): Unique user identifier
#         updates (dict): Dictionary of fields to update and their new values
#     """
#     user_ref = db.collection("users").document(user_id)
#     user_ref.update(updates)
#     print(f"[Firestore] Updated user profile for user_id: {user_id} with fields: {list(updates.keys())}")

# def delete_user_profile(user_id: str):
#     """
#     Delete a user profile document from Firestore.
    
#     Args:
#         user_id (str): Unique user identifier
#     """
#     user_ref = db.collection("users").document(user_id)
#     user_ref.delete()
#     print(f"[Firestore] Deleted user profile for user_id: {user_id}")

# def user_exists(user_id: str) -> bool:
#     """
#     Check if a user profile exists in Firestore.
    
#     Args:
#         user_id (str): Unique user identifier
        
#     Returns:
#         bool: True if user exists, False otherwise
#     """
#     user_ref = db.collection("users").document(user_id)
#     exists = user_ref.get().exists
#     print(f"[Firestore] User exists check for user_id: {user_id} = {exists}")
#     return exists

# def get_users_by_role(role: str) -> list[dict]:
#     """
#     Query and retrieve all user profiles with a specific role.
    
#     Args:
#         role (str): Role to filter users by (e.g., 'student', 'teacher')
        
#     Returns:
#         List[dict]: List of user profiles matching the role
#     """
#     users_ref = db.collection("users")
#     query = users_ref.where("role", "==", role)
#     docs = query.stream()
#     users = [doc.to_dict() for doc in docs]
#     print(f"[Firestore] Retrieved {len(users)} users with role '{role}'")
#     return users

# def update_user_settings(user_id: str, settings: dict):
#     """
#     Update or add nested 'settings' field inside a user profile document.
    
#     Args:
#         user_id (str): Unique user identifier
#         settings (dict): Dictionary of settings/preferences to save
#     """
#     user_ref = db.collection("users").document(user_id)
#     user_ref.update({"settings": settings})
#     print(f"[Firestore] Updated settings for user_id: {user_id}")





    from firebase_admin import firestore
from firestore.firebase_config import db

# -------------------------------
# Lesson Planner Agent
# -------------------------------
def create_lesson_plan(user_id: str, plan_data: dict):
    db.collection("lesson_plans").add({
        **plan_data,
        "user_id": user_id,
        "created_at": firestore.SERVER_TIMESTAMP
    })

def get_lesson_plans(user_id: str):
    return [doc.to_dict() for doc in db.collection("lesson_plans").where("user_id", "==", user_id).stream()]

# -------------------------------
# Story Teller Agent
# -------------------------------
def save_story(user_id: str, story_data: dict):
    db.collection("stories").add({
        **story_data,
        "user_id": user_id,
        "created_at": firestore.SERVER_TIMESTAMP
    })

def get_stories(user_id: str):
    return [doc.to_dict() for doc in db.collection("stories").where("user_id", "==", user_id).stream()]

# -------------------------------
# Course Planner Agent
# -------------------------------
def save_course_plan(user_id: str, course_data: dict):
    db.collection("course_plans").add({
        **course_data,
        "user_id": user_id,
        "created_at": firestore.SERVER_TIMESTAMP
    })

# -------------------------------
# Quiz Agent
# -------------------------------
def save_quiz_result(user_id: str, quiz_data: dict):
    db.collection("quiz_results").add({
        **quiz_data,
        "user_id": user_id,
        "submitted_at": firestore.SERVER_TIMESTAMP
    })

def get_quiz_results(user_id: str):
    return [doc.to_dict() for doc in db.collection("quiz_results").where("user_id", "==", user_id).stream()]

# -------------------------------
# Voice Tutor Agent
# -------------------------------
def log_voice_session(user_id: str, session_data: dict):
    db.collection("voice_sessions").add({
        **session_data,
        "user_id": user_id,
        "timestamp": firestore.SERVER_TIMESTAMP
    })

# -------------------------------
# Visual Agent
# -------------------------------
def save_visual_asset(user_id: str, visual_data: dict):
    db.collection("visual_assets").add({
        **visual_data,
        "user_id": user_id,
        "created_at": firestore.SERVER_TIMESTAMP
    })

# -------------------------------
# Ask Me Agent
# -------------------------------
def log_qa(user_id: str, question: str, answer: str):
    db.collection("qa_sessions").add({
        "user_id": user_id,
        "question": question,
        "answer": answer,
        "asked_at": firestore.SERVER_TIMESTAMP
    })

# -------------------------------
# Sync Agent
# -------------------------------
def log_sync_event(user_id: str, sync_data: dict):
    db.collection("sync_events").add({
        **sync_data,
        "user_id": user_id,
        "synced_at": firestore.SERVER_TIMESTAMP
    })

# -------------------------------
# Teacher Dashboard Agent
# -------------------------------
def record_teacher_metrics(user_id: str, dashboard_data: dict):
    db.collection("teacher_dashboards").add({
        **dashboard_data,
        "user_id": user_id,
        "recorded_at": firestore.SERVER_TIMESTAMP
    })

# -------------------------------
# Content Creator Agent
# -------------------------------
def save_generated_content(user_id: str, content_data: dict):
    db.collection("generated_content").add({
        **content_data,
        "user_id": user_id,
        "generated_at": firestore.SERVER_TIMESTAMP
    })

# -------------------------------
# Gamification Agent
# -------------------------------
def save_game_result(user_id: str, game_data: dict):
    db.collection("game_results").add({
        **game_data,
        "user_id": user_id,
        "played_at": firestore.SERVER_TIMESTAMP
    })

# -------------------------------
# Predictive Analytics Agent
# -------------------------------
def save_prediction(user_id: str, prediction_data: dict):
    db.collection("analytics_predictions").add({
        **prediction_data,
        "user_id": user_id,
        "predicted_at": firestore.SERVER_TIMESTAMP
    })

# -------------------------------
# Multimodal Research Agent
# -------------------------------
def log_multimodal_result(user_id: str, research_data: dict):
    db.collection("multimodal_research").add({
        **research_data,
        "user_id": user_id,
        "generated_at": firestore.SERVER_TIMESTAMP
    })

# -------------------------------
# Student-Level Analytics Agent
# -------------------------------
def log_student_analytics(user_id: str, analytics_data: dict):
    db.collection("student_analytics").add({
        **analytics_data,
        "user_id": user_id,
        "recorded_at": firestore.SERVER_TIMESTAMP
    })

