📄 CV Scanner

A web application that scans uploaded PDF cover letters to redact sensitive information and extract relevant skills. Built with a FastAPI backend and a React (Vite) frontend.

🚀 Features

✅ Upload PDF cover letters

✅ Redacts names and personal identifiers

✅ Extracts skills mentioned in the letter

✅ Clean, responsive UI with instant feedback

## 🛠️ Setup Instructions
   ```bash
   python -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn backend.api:app --reload
   ```