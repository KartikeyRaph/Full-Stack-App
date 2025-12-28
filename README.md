# Full Stack App — React + FastAPI + SQLite (CRUD sample)

This repository is a production-ready starter for a simple project tracker (CRUD).

- Backend: FastAPI + SQLModel (SQLite) — API served at `http://localhost:8000`.
- Frontend: React + Vite — dev server at `http://localhost:5173`.

Core entity: **Project** — fields: `title`, `description`, `status`, `priority`, `created_at`.

Quick start (Windows cmd.exe):

1) Backend
```
cd "full-stack_app\\backend"
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

2) Frontend
```
cd "full-stack_app\\frontend"
npm install
npm run dev
```

API (JSON)
- GET /api/projects
- POST /api/projects
- GET /api/projects/{id}
- PUT /api/projects/{id}
- DELETE /api/projects/{id}

Notes:
- CORS enabled for local development (vite proxy configured).
- SQLite file is created at `backend/database.db`.
- No authentication included — intended as a starter template you can extend.

If you’d like, I can add Dockerfiles, CI configuration, or extend the data model.