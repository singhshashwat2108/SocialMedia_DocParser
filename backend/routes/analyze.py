from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services.ai_service import analyze_social_content

router = APIRouter(
    prefix="/analyze",
    tags=["Analyze"]
)


class AnalyzeRequest(BaseModel):
    text: str


@router.post("")
async def analyze_text(request: AnalyzeRequest):
    result = analyze_social_content(request.text)

    if not result["success"]:
        raise HTTPException(status_code=502, detail=result["error"])

    return result["data"]
