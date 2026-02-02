from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import shutil

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("")
def upload_contract(file: UploadFile = File(...)):
    """
    Upload a contract PDF to server storage.
    """
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are supported"}

    data_dir = Path("data/uploads")
    data_dir.mkdir(parents=True, exist_ok=True)

    file_path = data_dir / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "File uploaded successfully",
        "pdf_path": str(file_path),
    }
