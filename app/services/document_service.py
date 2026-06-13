from pathlib import Path
from fastapi import UploadFile
from llama_index.core import SimpleDirectoryReader
import shutil
import os

from app.core.exceptions import DocumentNotFoundError

def load_documents(file_path: Path):
    """
    Loads documents from a file or directory using LlamaIndex SimpleDirectoryReader.
    """
    if not file_path.exists():
        raise DocumentNotFoundError(f"Path not found: {file_path}")
        
    if file_path.is_dir():
        reader = SimpleDirectoryReader(input_dir=str(file_path), recursive=True)
    else:
        reader = SimpleDirectoryReader(input_files=[str(file_path)])
        
    return reader.load_data()

def load_uploaded_file(file: UploadFile, save_dir: Path) -> Path:
    """
    Saves an uploaded file to the local disk for processing.
    """
    save_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = save_dir / file.filename
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return file_path
