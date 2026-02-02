from fastapi import APIRouter
from api.schemas.request_response import HealthResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
def health_check():
    return {"status": "ok"}
