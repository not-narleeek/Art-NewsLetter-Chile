import shutil
import os
from pathlib import Path
from fastapi import UploadFile
from typing import Optional

UPLOAD_DIR = Path("backend/static/uploads")

# Ensure directory exists
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()

async def save_image(file: UploadFile, filename: str) -> Optional[str]:
    """
    Saves an uploaded file to the local storage.
    Returns the relative URL/path to the file.
    """
    if not file:
        return None
        
    # Basic extension validation
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        raise ValueError("Invalid image format")

    final_filename = f"{filename}{ext}"
    destination_path = UPLOAD_DIR / final_filename
    
    save_upload_file(file, destination_path)
    
    # In production, this would return a CDN URL or S3 key.
    # For now, we return a path consistent with StaticFiles mounting.
    return f"/static/uploads/{final_filename}"
