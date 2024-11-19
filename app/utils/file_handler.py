from sentence_transformers import SentenceTransformer
from fastapi import UploadFile, HTTPException
from PyPDF2 import PdfReader
import re
import os

UPLOAD_DIR = "./uploads"

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_file(file: UploadFile):
    # Validate file size (max 5MB)
    file.file.seek(0, os.SEEK_END)  # Move the pointer to the end of the file
    file_size = file.file.tell()   # Get the size of the file
    file.file.seek(0)              # Reset the pointer to the start of the file

    if file_size > 5 * 1024 * 1024:  # 5MB
        raise HTTPException(status_code=400, detail="File too large. Max size is 5MB.")

    # Save the file locally
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return file_path

def extract_text(file_path: str) -> str:
    """
    Extract text from a file. Supports PDF and TXT formats.
    """
    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        return " ".join(page.extract_text() for page in reader.pages if page.extract_text())
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

def generate_embeddings(text: str):
    sentences = re.split(r"[.?!\n]+", text.strip())
    
    # print(f"Generated sentences: {sentences}")  # Debug
    
    embeddings = model.encode(sentences, convert_to_tensor=True)
    
    # print(f"Generated embeddings shape: {embeddings.shape}")  # Debug
    
    return embeddings, sentences
