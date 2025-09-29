from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .src.pdf import process_pdf
from .src.scanner import process_cover_letter  # <-- import your scanner
import os

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Upload PDF endpoint
# -------------------------------
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDFs are allowed."}

    content = await file.read()
    print(f"Received file: {file.filename}, size: {len(content)} bytes")

    # Save temp PDF
    temp_dir = "redacted"
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, file.filename)
    with open(temp_path, "wb") as f:
        f.write(content)

    try:
        # Extract text from PDF
        raw_text = process_pdf(temp_path)
        # Redact PII and extract skills
        redacted_text, skills = process_cover_letter(raw_text)
        print("PDF processed successfully")
    except Exception as e:
        print("PDF processing failed:", e)
        return {"error": str(e)}

    return {"redacted": redacted_text, "skills": skills}


# -------------------------------
# Serve built frontend
# -------------------------------
frontend_dist = os.path.join(os.path.dirname(__file__), "frontend_dist")
frontend_dist = os.path.abspath(frontend_dist)
print("Serving frontend from:", frontend_dist)

app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")
