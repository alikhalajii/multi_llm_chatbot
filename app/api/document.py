from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

from app.core.db import get_db
from app.models.user_document import UserDocument
from app.schemas.document import DocumentOut
from app.services.embedding_service import generate_embedding

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=List[DocumentOut])
async def upload_documents(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    """ Upload documents and store their embeddings. """
    stored_files = []
    for file in files:
        content = (await file.read()).decode("utf-8")
        vector = generate_embedding(content)

        doc = UserDocument(
            filename=file.filename,
            content=content[:2000],   # store limited content
            content_vector=vector
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)

        stored_files.append(
            DocumentOut(
                id=doc.id,
                filename=doc.filename,
                content_preview=(doc.content[:100] + "...") if doc.content else "",
                vector_len=len(doc.content_vector) if doc.content_vector is not None else 0
            )
        )
        logger.info("📄 Uploaded document: %s (ID=%s)", doc.filename, doc.id)

    return stored_files


@router.get("/", response_model=List[DocumentOut])
def list_documents(db: Session = Depends(get_db)):
    """ List all uploaded documents. """
    docs = db.query(UserDocument).all()
    return [
        DocumentOut(
            id=d.id,
            filename=d.filename,
            content_preview=(d.content[:100] + "...") if d.content else "",
            vector_len=len(d.content_vector) if d.content_vector is not None else 0
        )
        for d in docs
    ]


@router.delete("/{doc_id}")
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    """ Delete a document by ID. """
    doc = db.query(UserDocument).filter(UserDocument.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document_ID not found")

    db.delete(doc)
    db.commit()
    logger.info("🗑️ Deleted document ID=%s filename=%s", doc_id, doc.filename)

    return {"message": f"Document {doc_id} deleted successfully"}
