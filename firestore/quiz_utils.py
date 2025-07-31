from firestore.firebase_config import db
from datetime import datetime

def post_quiz_result(teacher_uid: str, class_id: str, subject: str, quiz_data: dict):
    class_doc = db.collection("classes").document(class_id).get()
    if not class_doc.exists:
        raise ValueError("Class does not exist")

    student_ids = class_doc.to_dict().get("students", [])

    for student_id in student_ids:
        quiz_entry = {
            **quiz_data,
            "timestamp": datetime.utcnow(),
            "subject": subject,
            "class_id": class_id,
            "student_id": student_id,
            "teacher_id": teacher_uid
        }

        db.collection("quiz_results").add(quiz_entry)
        db.collection("classes").document(class_id).collection("quiz_results").add(quiz_entry)
