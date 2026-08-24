# Social Media Content Analyzer

Upload a PDF or image of a social media post and get AI-powered engagement analysis and improvement suggestions.

## Features

- PDF upload
- Image upload (JPG/PNG/WEBP)
- OCR via Tesseract
- Direct PDF text extraction via PyMuPDF
- AI engagement analysis via Google Gemini
- Improvement suggestions
- Rewritten post output

## Tech stack

- Python
- FastAPI
- Tesseract OCR
- PyMuPDF
- Google Gemini (`google-genai`)
- Plain HTML/CSS/JS frontend

## Setup

1. Clone the repo
2. `pip install -r requirements.txt`
3. Install Tesseract: https://github.com/UB-Mannheim/tesseract/wiki and add it to PATH
4. Copy `.env.example` to `.env` and add your `GEMINI_API_KEY`
5. `uvicorn backend.app:app --reload`
6. Open http://localhost:8000

## Environment variables

| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | API key for Google Gemini, used to generate the engagement analysis |

## Getting a Gemini API key

Create a free key at https://aistudio.google.com and paste it into your `.env` file as `GEMINI_API_KEY`.
