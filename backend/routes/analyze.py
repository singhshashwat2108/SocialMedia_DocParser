from fastapi import APIRouter
from pydantic import BaseModel

from services.ai_service import analyze_social_content

router = APIRouter(
    prefix="/analyze",
    tags=["Analyze"]
)


class AnalyzeRequest(BaseModel):
    text: str


@router.post("")
async def analyze_text(request: AnalyzeRequest):
    return analyze_social_content(request.text)
