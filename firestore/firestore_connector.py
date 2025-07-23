from firebase_admin import credentials, firestore, initialize_app
import os

# Initialize the app with the default credentials from env variable
initialize_app()

db = firestore.client()
