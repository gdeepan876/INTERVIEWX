<<<<<<< HEAD
# INTERVIEWX – AI Interview Simulator

> **A professional, full-stack AI interview practice platform designed to simulate high-stakes technical and HR interviews with multi-dimensional scoring, dynamic follow-ups, and diagnostic reporting.**

---

## 📌 Project Overview

**INTERVIEWX** simulates real-world hiring loops for software engineering candidates and HR professionals. Candidates select their role, interview format, and difficulty level, and interact directly with a simulated interviewer.

### Key Capabilities:
- 🎯 **Role Specializations**: Curated tracks for **Java Developer**, **Python Developer**, **Frontend Developer**, and **Backend Developer**.
- 💼 **Interview Formats**: Deep **Technical** interviews (system design, concurrency, frameworks, trade-offs) and **HR / Behavioral** interviews (STAR methodology, conflict resolution, ownership).
- 📈 **3 Difficulty Levels**: **Beginner** (0-2 years), **Intermediate** (2-5 years), and **Advanced** (5+ years).
- ⚖️ **Objective 10-Point Scoring Rubric**: Every answer is evaluated against four criteria:
  1. *Correctness* (0 – 2.5 pts)
  2. *Relevance* (0 – 2.5 pts)
  3. *Clarity* (0 – 2.5 pts)
  4. *Technical Depth* (0 – 2.5 pts)
- 🔄 **Adaptive Follow-Up Questions**: Generates context-aware follow-up probes when an answer requires deeper technical substantiation.
- 📊 **Diagnostic Performance Report**: Delivers an executive summary, itemized candidate strengths, areas for improvement, and a tailored study roadmap.
- 🗄️ **Persistent Interview History**: Tracks past sessions and reports in a local SQLite database.
- 📱 **Responsive Design**: Clean desktop and mobile layouts styled with an authoritative Navy Blue (`#0F172A`), Pure White (`#FFFFFF`), and Subtle Purple (`#7C3AED`) palette.

---

## 🏛️ Beginner-Friendly Architecture Explanation

If you are new to web development and AI applications, here is a simple breakdown of how INTERVIEWX functions:

```
[Candidate's Browser]
        │
   React Frontend (HTML, CSS, JavaScript)
   Displays question cards, text answer box, score badges & diagnostic reports
        │
        │ HTTP REST Requests (JSON)
        ▼
[Python FastAPI Backend Server (Port 8000)]
   Session Manager ──► Question Bank ──► Heuristic/AI Evaluator
        │                                      │
   Reads & Writes Session History              Future Phase 4 Integration:
        │                                      Google Gemini API
        ▼
[SQLite Database (interviewx.db)]
   Normalized tables: interviews, questions, answers, evaluations, reports
```

- **Frontend (`frontend/`)**: Built with **React** and **Vite**. Provides a distraction-free, responsive interview console with instant state updates.
- **Backend (`backend/`)**: Built with **Python** and **FastAPI**. High performance, asynchronous request handling, and Pydantic schema validation.
- **Database**: Local **SQLite** database using SQLAlchemy ORM. Zero complex setup—runs right inside the repository.
- **AI Intelligence**: Structured service layer (`evaluation_service.py`). In this phase, it runs an intelligent heuristic rule-based evaluator that transparently assesses responses. **Google Gemini LLM integration is planned for Phase 4.**

---

## 📂 Project Directory Structure

```
INTERVIEWX/
├── PRD.md                                 # Full Product Requirements Document
├── README.md                              # Installation and setup instructions
├── .gitignore                             # Git ignore rules
│
├── backend/                               # Python FastAPI Application
│   ├── .env.example                       # Environment variables template
│   ├── requirements.txt                   # Backend dependencies
│   ├── main.py                            # FastAPI entry point, CORS & health check
│   ├── config.py                          # Settings reader (Pydantic BaseSettings)
│   ├── test_backend.py                    # Comprehensive backend integration test suite
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── session.py                     # SQLite engine & session dependency
│   │   └── models.py                      # SQLAlchemy models (Interview, Question, Answer, etc.)
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── interview.py                   # Pydantic validation schemas (requests & responses)
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── question_bank.py               # Curated question & follow-up pool for all 4 roles
│   │   ├── evaluation_service.py          # 4-pillar evaluation rubric & report synthesizer
│   │   └── interview_service.py           # Core business logic orchestrating the interview loop
│   │
│   └── routers/
│       ├── __init__.py
│       └── interview_router.py            # REST endpoints (/api/interviews)
│
└── frontend/                              # React + Vite Application
    ├── package.json                       # Frontend dependencies & scripts
    ├── vite.config.js                     # Vite proxy & build settings
    ├── index.html                         # HTML entry
    │
    └── src/
        ├── main.jsx                       # React DOM entry
        ├── App.jsx                        # Root state & navigation router
        ├── index.css                      # Design tokens (Navy, White, Purple)
        ├── App.css                        # Component layouts, cards, buttons & grids
        │
        ├── services/
        │   └── api.js                     # Backend API client with error handling
        │
        ├── components/
        │   ├── Navbar.jsx                 # Header with navigation & dev mode badge
        │   ├── Footer.jsx                 # Footer component
        │   ├── ProgressBar.jsx            # Progress bar for interview questions
        │   ├── ScoreBadge.jsx             # Color-coded score pill (High / Mid / Low)
        │   ├── QuestionCard.jsx           # Interviewer prompt card with metadata
        │   └── FeedbackCard.jsx           # Immediate score breakdown & suggestions
        │
        └── pages/
            ├── HomePage.jsx               # Landing page with feature overview
            ├── SetupPage.jsx              # Role, type, and difficulty selector
            ├── InterviewRoomPage.jsx      # Live interview text-based console
            ├── ReportPage.jsx             # Diagnostic report with strengths/weaknesses
            └── HistoryPage.jsx            # Session history table with SQLite persistence
```

---

## ⚙️ How to Run the Application Locally

Follow these step-by-step instructions to run INTERVIEWX on your local machine.

### Prerequisites:
- **Python**: Version 3.10 or higher
- **Node.js**: Version 18.0 or higher (with `npm`)

---

### Step 1: Start the Backend (FastAPI)

1. Open a terminal and navigate to the `backend` folder:
   ```bash
   cd backend
   ```

2. *(Optional but recommended)* Create and activate a Python virtual environment:
   ```bash
   # On Windows (PowerShell):
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # On macOS / Linux:
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create your local environment configuration file:
   ```bash
   # On Windows (PowerShell):
   Copy-Item .env.example .env

   # On macOS / Linux:
   cp .env.example .env
   ```

5. Launch the FastAPI development server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

6. Verify the backend is running:
   - Visit: [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)
   - Interactive Swagger API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### Step 2: Start the Frontend (React + Vite)

1. Open a **new terminal window** and navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```

2. Install the frontend dependencies:
   ```bash
   npm install
   ```

3. Start the Vite local development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to:
   **[http://localhost:5173](http://localhost:5173)**

---

## 🧪 Verification & Testing

### 1. Test Backend Core Integration:
```bash
python backend/test_backend.py
```

### 2. Test Live Gemini AI Endpoints:
```bash
python backend/test_ai_endpoints.py
```
This verifies:
- `POST /api/interviews/ai/generate-questions`: Generates tailored questions with key concepts using Gemini.
- `POST /api/interviews/ai/evaluate-answer`: Produces a 10-point evaluation, strengths, weaknesses, actionable suggestions, and an exemplary improved answer.

### 3. Verify Frontend Production Build:
```bash
npm run build --prefix frontend
```

---

## 🔍 Feature Status & Transparency

| Feature | Status | Notes |
| :--- | :---: | :--- |
| **Interactive UI (Home, Setup, Room, Report, History)** | ✅ Implemented | Fluid React SPA with responsive layout. |
| **Role Selection (Java, Python, Frontend, Backend)** | ✅ Implemented | Dedicated question banks for each role. |
| **Difficulty Scaling (Beginner, Intermediate, Advanced)** | ✅ Implemented | Calibrated question depth and rubric targets. |
| **Interview Types (Technical & HR)** | ✅ Implemented | Frameworks/syntax vs STAR behavioral scenarios. |
| **10-Point Evaluation Engine** | ✅ Implemented | Scores Correctness, Relevance, Clarity, and Depth. |
| **Adaptive Follow-up Questions** | ✅ Implemented | Triggers follow-ups based on response depth. |
| **Diagnostic Performance Report** | ✅ Implemented | Itemizes strengths, weaknesses, and next steps. |
| **SQLite History Persistence** | ✅ Implemented | Full session storage and report retrieval. |
| **Google Gemini LLM Integration** | ✅ Implemented | Connected via `google-genai` SDK using `gemini-3.1-flash-lite`. |

---

## 🧭 Testing Endpoints via Swagger UI (http://127.0.0.1:8000/docs)

Once the backend is started, open your browser and navigate to **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**.

### 1. Test Question Generation:
- Locate the **AI Integration** section.
- Expand `POST /api/interviews/ai/generate-questions`.
- Click **"Try it out"**.
- Modify the JSON payload (e.g., set `"role": "Java Developer"`, `"difficulty": "Intermediate"`, `"count": 3`).
- Click **"Execute"** to view real-time questions generated by Gemini.

### 2. Test Answer Evaluation:
- Expand `POST /api/interviews/ai/evaluate-answer`.
- Click **"Try it out"**.
- Input a question and a candidate answer.
- Click **"Execute"** to receive the 10-point score, itemized strengths, weaknesses, and an improved model answer.

---

## 📄 License
This project is open-source and available for educational and interview preparation purposes.

=======
# INTERVIEWX
>>>>>>> 6e96178c1faf7a05e12381f0a19884f0be37d79c
