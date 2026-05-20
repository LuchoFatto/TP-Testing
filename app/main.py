from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routes.auth import router as auth_router
from app.routes.events import router as events_router
from app.routes.orders import router as orders_router


BASE_DIR = Path(__file__).resolve().parents[1]
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Simple Testing Project", version="0.1.0")
app.include_router(auth_router)
app.include_router(events_router)
app.include_router(orders_router)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")
