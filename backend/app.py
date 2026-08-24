import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.routes.upload import router as upload_router
from backend.routes.analyze import router as analyze_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(analyze_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


@app.on_event("startup")
async def check_frontend_dir():
    if FRONTEND_DIR.exists():
        files = [f.name for f in FRONTEND_DIR.iterdir()]
        logger.info("Frontend directory found at %s: %s", FRONTEND_DIR, files)
    else:
        logger.error("Frontend directory NOT found at %s", FRONTEND_DIR)


@app.get("/")
async def root():
    return FileResponse(str(FRONTEND_DIR / "index.html"))


app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")
