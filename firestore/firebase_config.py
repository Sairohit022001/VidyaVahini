import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Path to the Firebase Admin SDK JSON key from .env
firebase_key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Initialize Firebase app
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_key_path)
    firebase_admin.initialize_app(cred)

# Get Firestore DB client
db = firestore.client()
