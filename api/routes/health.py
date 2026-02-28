import os
from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter()
_STARTED_AT = datetime.now(timezone.utc)


@router.get("")
def health():
    now = datetime.now(timezone.utc)
    return {
        "status": "ok",
        "service": "samvidai-api",
        "checks": {
            "api": "ok",
            "gemini_key_configured": bool(os.getenv("GEMINI_API_KEY")),
        },
        "time": {
            "started_at_utc": _STARTED_AT.isoformat(),
            "now_utc": now.isoformat(),
            "uptime_seconds": int((now - _STARTED_AT).total_seconds()),
        },
    }


@router.get("/ready")
def readiness():
    key_ok = bool(os.getenv("GEMINI_API_KEY"))
    return {
        "status": "ready" if key_ok else "degraded",
        "checks": {
            "gemini_key_configured": key_ok,
        },
    }
