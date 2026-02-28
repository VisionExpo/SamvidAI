from typing import Literal, Optional

from pydantic import BaseModel, Field


class UploadIngestionResult(BaseModel):
    status: Literal["success", "failed", "skipped"]
    chunks_created: int = 0
    error: Optional[str] = None


class UploadStorageInfo(BaseModel):
    persisted_pdf: bool = False
    pdf_virtual_path: str
    index_dir: Optional[str] = None


class UploadResponse(BaseModel):
    status: Literal["uploaded"]
    upload_id: str
    filename: str
    content_type: str
    size_bytes: int = Field(ge=0)
    data_source: str
    index_id: Optional[str] = None
    pdf_path: str
    ingestion_status: Literal["success", "failed", "skipped"]
    ingestion_error: Optional[str] = None
    chunks_created: int = 0
    ingestion: UploadIngestionResult
    storage: UploadStorageInfo
