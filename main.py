from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
from app.core.database import engine, Base, get_db
from app.models import subtask as _subtask_model  # register SubTask table
from app.models import station as _station_model    # register PoliceStation table
from app.routers import auth, officers, tasks, stats
from app.routers import admin as admin_router
from app.routers import subtasks as subtasks_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="PTMS", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,         prefix="/api/auth",    tags=["Auth"])
app.include_router(officers.router,     prefix="/api/officers",tags=["Officers"])
app.include_router(tasks.router,        prefix="/api/tasks",   tags=["Tasks"])
app.include_router(stats.router,        prefix="/api/stats",   tags=["Stats"])
app.include_router(admin_router.router,         prefix="/api/admin",         tags=["Admin"])
app.include_router(subtasks_router.router,     prefix="/api/tasks",         tags=["SubTasks"])
from app.routers import stations as stations_router
app.include_router(stations_router.router,     prefix="/api/stations",      tags=["Stations"])


FRONTEND      = Path(__file__).resolve().parent.parent / "index.html"
SW_FILE       = Path(__file__).resolve().parent.parent / "service-worker.js"
MANIFEST_FILE = Path(__file__).resolve().parent.parent / "manifest.json"
ICON_FILE     = Path(__file__).resolve().parent.parent / "icon-192.png"


@app.on_event("startup")
def ensure_admin():
    """Ensure ADMIN officer exists in DB and passwords.json on every startup."""
    import json, bcrypt
    from sqlalchemy.orm import Session
    from app.models.officer import Officer
    from app.core.file_store import PASSWORDS_FILE

    db = next(get_db())
    try:
        admin = db.query(Officer).filter(Officer.id == "ADMIN").first()
        if not admin:
            db.add(Officer(
                id="ADMIN", name="System Admin", rank="Admin",
                level=99, report_to=None, password_hash="file_managed",
            ))
            db.commit()

        data = {}
        if PASSWORDS_FILE.exists():
            data = json.loads(PASSWORDS_FILE.read_text())
        if "ADMIN" not in data:
            data["ADMIN"] = bcrypt.hashpw(b"admin1234", bcrypt.gensalt(12)).decode()
            PASSWORDS_FILE.write_text(json.dumps(data, indent=2))
    except Exception as e:
        print(f"[startup] Admin init: {e}")
    finally:
        db.close()


@app.get("/")
def serve_frontend():
    return FileResponse(FRONTEND)

@app.get("/service-worker.js")
def serve_sw():
    return FileResponse(SW_FILE, media_type="application/javascript")

@app.get("/manifest.json")
def serve_manifest():
    return FileResponse(MANIFEST_FILE, media_type="application/json")

@app.get("/icon-192.png")
def serve_icon():
    if ICON_FILE.exists():
        return FileResponse(ICON_FILE, media_type="image/png")
    from fastapi.responses import Response
    return Response(status_code=404)
