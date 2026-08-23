import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.upload import router as upload_router
from routes.analyze import router as analyze_router

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(analyze_router)


@app.get("/")
def home():
    return {"index.html"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
