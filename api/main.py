from fastapi import FastAPI
from api.routes import analyze, health, upload

app = FastAPI(
    title="SamvidAI",
    description="Intelligent Contract Analysis Engine",
    version="1.0.0",
)


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
