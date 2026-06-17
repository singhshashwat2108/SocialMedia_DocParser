from pydantic import BaseModel

class OCRWord(BaseModel):
    text: str
    bbox: list[list[float]]
    confidence: float