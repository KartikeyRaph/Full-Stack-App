# Full Stack App — React + FastAPI + SQLite (CRUD sample)

This repository is a production-ready starter for a simple project tracker (CRUD).

- Backend: FastAPI + SQLModel (SQLite) — API served at `http://localhost:8000`.
- Frontend: React + Vite — dev server at `http://localhost:5173`.

Core entity: **Project** — fields: `title`, `description`, `status`, `priority`, `created_at`.

Quick start (Windows cmd.exe):

1) Backend
```

Environment (.env)
1. Copy the example file in the backend folder:
	- `cd full-stack_app/backend` then `copy .env.example .env` (Windows)
2. Edit `.env` and set `HOST`, `PORT`, and optionally `FRONTEND_URL` (the frontend origin) if needed.
3. To serve a built frontend from the backend (production), build the frontend and set `FRONTEND_BUILD_DIR` in the backend `.env` (defaults to `../frontend/dist`).

Production serving example:

1. Build frontend:
```
cd full-stack_app/frontend
npm install
npm run build
```

2. Ensure the backend knows where the build is (either leave default or set explicit env):
```
cd full-stack_app/backend
copy .env.example .env
rem set FRONTEND_BUILD_DIR=..\frontend\dist
python -m app.main
```

When a `dist` directory is present, the backend will mount the static files at `/` and serve the React app while exposing `/api/*` endpoints for the API.
cd "full-stack_app\\backend"
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
# Option A: use uvicorn and pass HOST/PORT via env vars
# Windows cmd.exe example:
# set HOST=0.0.0.0 & set PORT=8000 & uvicorn app.main:app --reload --host %HOST% --port %PORT%
# Option B: run the module which will pick HOST/PORT from .env or env vars
python -m app.main
```

2) Frontend
```

Environment (.env)
1. Copy the example in the frontend folder:
	- `cd full-stack_app/frontend` then `copy .env.example .env` (Windows)
2. Edit `.env` and set `VITE_API_URL` if you want the front-end to call a specific backend host (e.g. `http://192.168.1.10:8000/api`).
cd "full-stack_app\\frontend"
npm install
# Optionally configure the backend API url in .env (VITE_API_URL)
# e.g. VITE_API_URL=http://192.168.1.10:8000/api
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