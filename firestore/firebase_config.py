import os
import firebase_admin
from firebase_admin import credentials, firestore

# ✅ Load key file path dynamically
key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
cred = credentials.Certificate(key_path)

# ✅ Safe init: only initialize if not already initialized
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# ✅ Get Firestore client
db = firestore.client()
