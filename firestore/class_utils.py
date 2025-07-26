from firestore_connector import db
from datetime import datetime
from google.cloud import firestore

def create_class(class_id: str, class_data: dict, teacher_uid: str, subject: str):
    db.collection("classes").document(class_id).set({
        **class_data,
        "students": [],
        "subjects": {subject: teacher_uid},
        "created_at": datetime.utcnow(),
    })

    teacher_ref = db.collection("users").document(teacher_uid)
    teacher_doc = teacher_ref.get().to_dict()
    teacher_classes = teacher_doc.get("teacherOf", [])
    if class_id not in teacher_classes:
        teacher_classes.append(class_id)
    teacher_ref.update({"teacherOf": teacher_classes})

def add_student_to_class(class_id: str, student_id: str):
    class_ref = db.collection("classes").document(class_id)
    student_ref = db.collection("students").document(student_id)

    if not class_ref.get().exists or not student_ref.get().exists:
        raise ValueError("Class or student not found")

    class_ref.update({"students": firestore.ArrayUnion([student_id])})
    student_ref.update({"linked_classes": firestore.ArrayUnion([class_id])})
