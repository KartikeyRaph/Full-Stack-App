import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import logging

from sqlmodel import Session, select
from dotenv import load_dotenv

load_dotenv()

from .database import engine, init_db
from .models import Project

app = FastAPI(
    title="ProjectPulse API",
    description="ProjectPulse — a focused project tracking backend (FastAPI + SQLite). Designed as a production-ready starter.",
    version="1.0.0",
)

# CORS
frontend_url = os.getenv('FRONTEND_URL')
allow_origins = ["http://localhost:5173", "http://localhost:3000"]
if frontend_url:
    allow_origins.insert(0, frontend_url)
allow_origins.append("*")  # Remove or tighten in real production

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====================
# ALL API ROUTES FIRST
# ====================

@app.get("/api/projects")
def list_projects():
    with Session(engine) as session:
        projects = session.exec(
            select(Project).order_by(Project.priority, Project.created_at)
        ).all()
        return projects


@app.post("/api/projects", status_code=201)
def create_project(project: Project):
    with Session(engine) as session:
        new_project = Project(
            title=project.title,
            description=project.description or "",
            status=project.status or "idea",
            priority=project.priority or 2
        )
        session.add(new_project)
        session.commit()
        session.refresh(new_project)
        return new_project


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


# Database startup and seeding
@app.on_event("startup")
def on_startup():
    init_db()
    with Session(engine) as session:
        if not session.exec(select(Project)).first():
            welcome = Project(
                title="Welcome: Example Project",
                description="This project was created as a starter sample.",
                status="active",
                priority=1
            )
            session.add(welcome)
            session.commit()
            logging.getLogger("uvicorn.error").info("Seeded welcome project")


# ============================
# FRONTEND SERVING (LAST!)
# ============================

logger = logging.getLogger("uvicorn.error")
root = Path(__file__).resolve().parents[2]  # Full-Stack-App root
default_build = root / "frontend" / "dist"
build_dir = os.getenv("FRONTEND_BUILD_DIR") or str(default_build)
build_path = Path(build_dir)

if build_path.exists() and build_path.is_dir():
    # Serve Vite assets (JS/CSS) at /assets
    assets_path = build_path / "assets"
    if assets_path.exists() and assets_path.is_dir():
        app.mount("/assets", StaticFiles(directory=str(assets_path)), name="assets")

    # Root → index.html
    @app.get("/")
    async def serve_root():
        return FileResponse(str(build_path / "index.html"))

    # Catch-all fallback for React Router — MUST be last
    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="Not Found")
        return FileResponse(str(build_path / "index.html"))

    logger.info(f"Frontend serving enabled from {build_path}")
else:
    logger.warning(f"Frontend build not found at {build_path}. Run 'npm run build' in frontend/")

# Development runner
if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("app.main:app", host=host, port=port, reload=True)