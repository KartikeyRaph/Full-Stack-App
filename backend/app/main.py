import os
from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import logging

# Load .env from backend folder if present
load_dotenv()

from .database import engine, init_db
from .models import Project

app = FastAPI(
    title="ProjectPulse API",
    description="ProjectPulse — a focused project tracking backend (FastAPI + SQLite). Designed as a production-ready starter.",
    version="1.0.0",
)

# CORS: use FRONTEND_URL from env if provided, otherwise allow common dev origins
frontend_url = os.getenv('FRONTEND_URL')
allow_list = ["http://localhost:5173", "http://localhost:3000"]
if frontend_url:
    allow_list.insert(0, frontend_url)
else:
    allow_list.append("*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend static files if a build is available
logger = logging.getLogger("uvicorn.error")
root = Path(__file__).resolve().parents[2]  # full-stack_app
default_build = root / 'frontend' / 'dist'
build_dir = os.getenv('FRONTEND_BUILD_DIR') or str(default_build)
build_path = Path(build_dir)
if build_path.exists() and build_path.is_dir():
    app.mount("/", StaticFiles(directory=str(build_path), html=True), name="frontend")
    logger.info(f"Mounted frontend static files from {build_path}")
else:
    logger.debug(f"Frontend build not found at {build_path}; static files not mounted. Build the frontend and set FRONTEND_BUILD_DIR if needed.")


@app.on_event("startup")
def on_startup():
    init_db()
    # seed a project if empty
    with Session(engine) as session:
        existing = session.exec(select(Project)).first()
        if not existing:
            p = Project(title="Welcome: Example Project",
                        description="This project was created as a starter sample.",
                        status="active",
                        priority=1)
            session.add(p)
            session.commit()


if __name__ == '__main__':
    # Allow running `python -m app.main` during development and pick host/port from env
    import uvicorn
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', '8000'))
    uvicorn.run('app.main:app', host=host, port=port, reload=True)


@app.get("/api/projects")
def list_projects():
    with Session(engine) as session:
        projects = session.exec(select(Project).order_by(Project.priority, Project.created_at)).all()
        return projects


@app.post("/api/projects", status_code=201)
def create_project(project: Project):
    with Session(engine) as session:
        new = Project(title=project.title, description=project.description or "", status=project.status or "idea", priority=project.priority or 2)
        session.add(new)
        session.commit()
        session.refresh(new)
        return new


@app.get("/api/projects/{project_id}")
def get_project(project_id: int):
    with Session(engine) as session:
        project = session.get(Project, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project


@app.put("/api/projects/{project_id}")
def update_project(project_id: int, updated: Project):
    with Session(engine) as session:
        project = session.get(Project, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        project.title = updated.title
        project.description = updated.description
        project.status = updated.status
        project.priority = updated.priority
        session.add(project)
        session.commit()
        session.refresh(project)
        return project


@app.delete("/api/projects/{project_id}", status_code=204)
def delete_project(project_id: int):
    with Session(engine) as session:
        project = session.get(Project, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        session.delete(project)
        session.commit()
        return None
