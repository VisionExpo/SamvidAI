from fastapi import FastAPI
from dotenv import load_dotenv
from pathlib import Path

# Load .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

from api.routes import analyze, health, upload
from api.errors import register_error_handlers

app = FastAPI(
    title="SamvidAI",
    description="Intelligent Contract Analysis Engine",
    version="1.0.0",
)
register_error_handlers(app)


@app.get("/")
def root():
    return {"message": "SamvidAI API is running"}


app.include_router(
    health.router,
    prefix="/health",
    tags=["Health"],
)

app.include_router(
    upload.router,
    prefix="/upload",
    tags=["Upload"],
)

app.include_router(
    analyze.router,
    prefix="/analyze",
    tags=["Analysis"],
)
