from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.user_document import UserDocument

router = APIRouter(tags=["debug"])


@router.get("/debug/docs")
async def list_docs(db: Session = Depends(get_db)) -> list[dict]:
    """ List all stored documents with basic info for debugging purposes. """
    docs = db.query(UserDocument).all()
    return [
        {
            "id": d.id,
            "filename": d.filename,
            "content_len": len(d.content or ""),
            "vector_dim": len(d.content_vector) if d.content_vector is not None else 0,
        }
        for d in docs
    ]
