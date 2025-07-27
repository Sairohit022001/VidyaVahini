# VidyaVāhinī

> **A Multilingual, Multimodal, Offline-First Education Platform powered by Agentic AI**

VidyaVāhinī is an AI-driven educational platform designed to deliver structured lessons, interactive quizzes, and voice-based tutoring across multiple Indian languages and dialects. It integrates advanced AI agents, offline-first architecture, and regional adaptation for personalized learning experiences.

---

## 🚀 Features

- **Agentic AI Architecture** – Modular agent-task-tool design.
- **Lesson Generation** – Topic-wise structured lessons (concepts, research references, summaries, and practice Q&A).
- **BhāṣāGuru Agent** – Regional dialect clustering, SSML prosody handling, and Google Cloud TTS voice synthesis.
- **Quiz & Assessment Engine** – Dynamic quiz creation aligned with student level and curriculum.
- **Offline-First Support** – IndexedDB + Firestore synchronization.
- **Multilingual Support** – Telugu (Andhra/Telangana), Hindi, English, and more.
- **Teacher & Student Dashboards** – Role-based analytics and content management.
- **FastAPI Backend + React Frontend** – Scalable architecture for production.
- **GCP Integration** – Google Cloud Text-to-Speech, Cloud Build, Artifact Registry.

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** (Python)
- **CrewAI** for agent orchestration
- **Google Cloud TTS**
- **Firestore**
- **Docker**

### Frontend
- **React (TypeScript)**
- **TailwindCSS**
- **IndexedDB for offline sync**
- **Firebase Auth (optional)**

---

## 📂 Project Structure


├── agents ├── app.yaml ├── crewflows ├── docker-compose.yml ├── Dockerfile ├── firestore ├── frontend ├── keys ├── list_models.py ├── llms ├── main.py ├── node_modules ├── package.json ├── payload.json ├── pycache ├── pytest.ini ├── README.md ├── requirements.txt ├── routes ├── tasks ├── telangana_dialect_map.json ├── test ├── tests ├── test_voice_tutor.py ├── tools ├── venv ├── vidyavahinifirebase ├── voice_tutor_output_andhra.mp3 └── voice_tutor_output_Telangana.mp3
---

## ⚙️ Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/<your-username>/VidyaVahini.git
cd VidyaVahini


### 2. Backend Setup
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export GOOGLE_APPLICATION_CREDENTIALS="path/to/vidyavahini-tts-27ed6a33108a.json"
uvicorn app:app --reload


### 3. Frontend Setup
cd frontend
npm install
npm run dev



📜 License
This project is licensed under the MIT License.

👥 Contributors

Rohi - AI Pipelines

Deepanshi – Frontend/Backend

Nanditha – Backend

Amritha – Frontend

Srujana – AI Pipelines
