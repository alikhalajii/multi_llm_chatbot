from fastapi import FastAPI

from app.core.db import Base, engine
from app.core.db_check import check_pgvector
from app.api import chatbot, document, debug
from app.core.logging_config import setup_logging

setup_logging()

app = FastAPI(title="Multi-LLM Chatbot API")


@app.on_event("startup")
async def startup_event() -> None:
    if engine.url.get_backend_name() == "postgresql":
        check_pgvector()


# Create database tables
Base.metadata.create_all(bind=engine)

# API Routes
app.include_router(document.router, prefix="/document", tags=["document"])
app.include_router(chatbot.router, prefix="/chat", tags=["chat"])
app.include_router(debug.router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "message": "Multi-LLM Chatbot backend is running.",
        "docs": "http://localhost:8000/docs",
        "gradio": "http://localhost:7860",
    }
