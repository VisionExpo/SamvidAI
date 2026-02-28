from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


def _request_id(request: Request) -> str:
    return request.headers.get("x-request-id", uuid4().hex)


def _error_body(
    request: Request,
    *,
    code: str,
    message: str,
    details,
    status: int,
):
    return {
        "error": {
            "code": code,
            "message": message,
            "details": details,
            "status": status,
            "path": request.url.path,
            "method": request.method,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "request_id": _request_id(request),
        }
    }


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content=_error_body(
                request,
                code="validation_error",
                message="Request validation failed",
                details=exc.errors(),
                status=422,
            ),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        detail = exc.detail
        message = detail if isinstance(detail, str) else "HTTP error"
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_body(
                request,
                code="http_error",
                message=message,
                details=detail,
                status=exc.status_code,
            ),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content=_error_body(
                request,
                code="internal_error",
                message="Internal server error",
                details={"type": exc.__class__.__name__},
                status=500,
            ),
        )
