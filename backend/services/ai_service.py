import json
import logging
import os

from google import genai
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

MODEL_NAME = "gemini-3.6-flash"

ANALYSIS_PROMPT_TEMPLATE = """You are analyzing a social media post. Given the text below, return ONLY raw JSON (no markdown, no code fences, no commentary) with exactly this shape:

{{
  "engagement_score": <integer 1-10>,
  "tone": "<short description of the tone>",
  "suggestions": ["<suggestion 1>", "<suggestion 2>", "<suggestion 3>"],
  "improved_version": "<a rewritten, improved version of the post>"
}}

Post:
\"\"\"{text}\"\"\"
"""


def _strip_markdown_fence(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1] if "\n" in raw else raw
        if raw.endswith("```"):
            raw = raw[: -len("```")]
    return raw.strip()


def analyze_social_content(text: str):
    if not text or not text.strip():
        return {"success": False, "error": "Text must not be empty"}

    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY is not configured")
        return {"success": False, "error": "GEMINI_API_KEY is not configured"}

    try:
        prompt = ANALYSIS_PROMPT_TEMPLATE.format(text=text)
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        raw = _strip_markdown_fence(response.text)
        analysis = json.loads(raw)

        logger.info(
            "Gemini analysis succeeded (%d chars in, score=%s)",
            len(text),
            analysis.get("engagement_score"),
        )
        return {"success": True, "data": analysis}

    except json.JSONDecodeError as exc:
        logger.exception("Gemini response was not valid JSON")
        return {"success": False, "error": f"Model returned invalid JSON: {exc}"}

    except Exception as exc:
        logger.exception("Gemini analysis failed")
        return {"success": False, "error": f"AI analysis failed: {exc}"}
