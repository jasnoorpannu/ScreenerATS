import pdfplumber
import docx
from fastapi import UploadFile
from utils.clean_text import clean_text_basic

def extract_text_from_resume(file: UploadFile) -> str:
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        return extract_from_pdf(file)
    elif filename.endswith(".docx"):
        return extract_from_docx(file)
    else:
        return ""

def extract_from_pdf(file: UploadFile) -> str:
    try:
        text = ""
        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text: 
                    text += page_text + "\n"

        if len(text.strip()) < 20:
            return "[ERROR] Scanned PDF detected. Please upload a text-based resume."

        return clean_text_basic(text)
    except Exception:
        return "[ERROR] Unable to extract text from PDF."

def extract_from_docx(file: UploadFile) -> str:
    try:
        doc = docx.Document(file.file)
        full_text = "\n".join([para.text for para in doc.paragraphs])
        return clean_text_basic(full_text)
    except Exception:
        return "[ERROR] Unable to extract text from DOCX."
