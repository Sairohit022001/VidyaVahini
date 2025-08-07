import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';  // <-- Add this import

const firebaseConfig = {
  apiKey: "AIzaSyAq9HDlF5eUvSSqXlZKtrYvw2TZTMH6A9k",
  authDomain: "firebase-adminsdk-fbsvc-eda4279973.json",
  projectId: "hackathon-demo-key-2025",
  storageBucket: "YOUR_STORAGE_BUCKET",
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  appId: "YOUR_APP_ID",
  measurementId: "YOUR_MEASUREMENT_ID",
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);
