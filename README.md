# EduEase: AI Adaptive Assistant

EduEase is a web app that helps students learn from their own study material. A student uploads a PDF and gets simplified text, auto-generated practice quizzes and an AI chatbot tutor. Students and teachers log in with separate roles.

## Features

| Feature | Status | Notes |
|---|---|---|
| Register / login with student or teacher role | Working | Firebase Auth; role stored in Firestore and enforced by `RoleGate` |
| PDF upload and text extraction | Working | PyPDF2 |
| Save and list content | Working | Firestore |
| Text simplification | Working (basic) | spaCy sentence splitting and lemmatization |
| Quiz generation | Working (rule-based) | Fill-in-the-blank MCQs built with spaCy POS tagging |
| AI chatbot | Working | LangChain + Gemini 2.5 Flash with conversation memory |
| Translation (Hindi / Tamil) | Code written, not wired up | Argos Translate in `backend/services/translate_service.py` |
| Teacher dashboard, eye tracking, recommendations, analytics | Placeholder | See `docs/future-work.md` |

## Architecture

```
┌──────────────────────────┐   REST (JSON / multipart)   ┌──────────────────────────┐
│  Frontend (browser)      │ ──────────────────────────▶ │  Backend (FastAPI)       │
│  React + TypeScript      │ ◀────────────────────────── │  localhost:8000          │
│  Vite, Tailwind, Zustand │                             │                          │
└───────┬──────────────────┘                             │  /upload-pdf   PyPDF2    │
        │ login / role lookup                            │  /simplify-text spaCy    │
        ▼                                                │  /generate-quiz spaCy    │
┌──────────────────────────┐   firebase-admin            │  /chatbot  LangChain     │
│  Firebase                │ ◀────────────────────────── │  /add-content            │
│  Auth + Firestore        │                             │  /get-content            │
└──────────────────────────┘                             └────────────┬─────────────┘
                                                                      │
                                                                      ▼
                                                           Google Gemini (LLM)
```

## Tech stack

**Frontend:** React 18, TypeScript, Vite, Tailwind CSS, React Router, Zustand, i18next, Axios, Firebase SDK

**Backend:** Python, FastAPI, Uvicorn, spaCy, PyPDF2, LangChain, Google Gemini (`langchain-google-genai`), Argos Translate, firebase-admin

**Services:** Firebase Authentication, Cloud Firestore

## Project structure

```
backend/
  app.py              FastAPI app and all active endpoints
  firebase_config.py  Firestore client (db is None if the key file is missing)
  routers/, services/ Modular layout, mostly placeholders for now
frontend/
  src/pages/          Login, Register, dashboards, Upload, Learning, Quiz
  src/components/     UploadForm, Chatbot, RoleGate, TTS/STT controls, etc.
  src/services/       Firebase and API helpers
docs/                 Demo script, ethics/privacy notes, future work
```

## Getting started

### Prerequisites
- Python 3.10+ and Node.js 18+
- A Firebase project (Auth and Firestore enabled)
- A Google AI (Gemini) API key

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

1. Download a service account key from the Firebase console and save it as `backend/serviceAccountKey.json`. It is git-ignored. Without it the backend still starts, but the content endpoints return a warning.
2. Set your Gemini API key in `backend/app.py`, in the `ChatGoogleGenerativeAI(...)` call. Do not commit real keys.

```bash
python app.py        # serves on http://localhost:8000
```

Interactive API docs are at http://localhost:8000/docs.

### Frontend

```bash
cd frontend
npm install
npm run dev          # serves on http://localhost:5173
```

Put your Firebase web config in `frontend/src/services/firebase.ts`.

## Known limitations

- The chatbot is a general tutor and does not yet answer from the uploaded PDF (RAG is planned).
- Chat memory is held in server memory and is shared across users.
- Backend endpoints do not verify Firebase ID tokens yet.
- Quiz and simplification are rule-based, so quality is limited.

## Future work

LLM-based quiz generation, retrieval over uploaded documents, per-user chat memory, translation endpoint, teacher analytics, and adaptive recommendations. See [docs/future-work.md](docs/future-work.md).
