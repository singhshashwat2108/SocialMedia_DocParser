from fastapi import FastAPI

from routes.upload import router as upload_router
from routes.analyze import router as analyze_router

app = FastAPI()

app.include_router(upload_router)
app.include_router(analyze_router)


@app.get("/")
def home():
    return {"index.html"}
