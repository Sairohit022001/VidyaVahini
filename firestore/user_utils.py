from firestore.firebase_config import db
from firebase_admin import auth
from datetime import datetime

def register_user(email: str, password: str, role: str, user_data: dict):
    user_record = auth.create_user(email=email, password=password)
    user_id = user_record.uid

    db.collection("users").document(user_id).set({
        "email": email,
        "role": role,
        **user_data,
        "created_at": datetime.utcnow()
    })

    if role == "student":
        db.collection("students").document(user_data["student_id"]).set({
            "uid": user_id,
            "name": user_data.get("name"),
            "email": email,
            "grade": user_data.get("grade"),
            "linked_classes": [],
            "added_by": None,
            "created_at": datetime.utcnow()
        })

    return user_id
