import mimetypes
import pdfplumber

def is_pdf(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type == "application/pdf"

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def process_pdf(file_path):
    if not is_pdf(file_path):
        raise ValueError(f"File {file_path} is not a PDF.")
    text = extract_text_from_pdf(file_path)
    return text
