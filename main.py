from fastapi import FastAPI

from routes.document import router as document_router

app = FastAPI()

app.include_router(document_router)


@app.get("/")
def home():
    return {"index.html"}