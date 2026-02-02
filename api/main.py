from fastapi import FastAPI

from api.routes.health import router as health_router
from api.routes.upload import router as upload_router
from api.routes.analyze import router as analyze_router

app = FastAPI(
    title="SamvidAI",
    version="1.0.0",
    description="OpticalRAG-based Legal Contract Analysis Engine",
)

app.include_router(health_router)
app.include_router(upload_router)
app.include_router(analyze_router)
