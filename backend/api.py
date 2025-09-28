from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import tempfile
import os

from backend.src.pdf import process_pdf
from backend.src.scanner import process_cover_letter

# Create FastAPI app
app = FastAPI()

# CORS middleware
# You can restrict origins to your deployed frontend URL if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_path = os.path.join(os.path.dirname(__file__), "frontend_dist")

app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

# Health check / root API route (optional)
@app.get("/api/health")
async def root():
    return {"message": "Backend is running"}

# PDF upload and processing endpoint
@app.post("/api/upload")
async def upload_cover_letter(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are allowed."}

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        raw_text = process_pdf(tmp_path)
        redacted, skills = process_cover_letter(raw_text)
        return {
            "redacted": redacted,
            "skills": skills,
        }
    except Exception as e:
        return {"error": str(e)}
