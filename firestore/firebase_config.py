import os
from dotenv import load_dotenv
from firebase_admin import credentials, initialize_app, firestore

load_dotenv()
cred_path = os.getenv("serviceAccountKey")
if not cred_path or not os.path.exists(cred_path):
    raise FileNotFoundError(f"Service account key file not found at: {cred_path}")

cred = credentials.Certificate(cred_path)
initialize_app(cred)

db = firestore.client()  # <--- Add this to initialize Firestore client and expose `db`
