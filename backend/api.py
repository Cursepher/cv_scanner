from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import tempfile

from backend.src.pdf import process_pdf
from backend.src.scanner import process_cover_letter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Backend is running"}


@app.post("/upload")
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
