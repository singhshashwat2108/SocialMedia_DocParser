# Approach

I built a Social Media Content Analyzer: you upload a PDF or image of a post, and it extracts the text and returns an AI-generated engagement score, tone, improvement suggestions, and a rewritten version.

I chose FastAPI for the backend because it gives async request handling and automatic request validation with minimal boilerplate, which suited a small pipeline of upload → extract → analyze steps. For text extraction, I chose Tesseract over EasyOCR specifically for startup time: EasyOCR loads a neural network on boot, adding 30-60 seconds and a large memory footprint, while Tesseract starts instantly.

The pipeline: a file is uploaded, then for PDFs I try PyMuPDF's direct text extraction first, since most PDFs already have selectable text and skipping OCR entirely is both faster and more accurate. Only if that comes back empty (a scanned PDF) or the file is an image do I fall back to Tesseract. The extracted text is then sent to Gemini for the actual analysis.

The main tradeoff is OCR accuracy: Tesseract is lighter but noticeably weaker than EasyOCR on low-quality or heavily stylized scans. There's also a small cold-start cost on the very first OCR call as Tesseract's runtime initializes.
