from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.db import get_db
from app.models.user_document import UserDocument
from app.schemas.document import DocumentOut
from app.services.embedding_service import generate_embedding

router = APIRouter()


@router.post("/", response_model=List[DocumentOut])
async def upload_documents(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    """ Endpoint to upload documents and store their embeddings. """
    stored_files = []
    for file in files:
        content = (await file.read()).decode("utf-8")
        vector = generate_embedding(content)

        doc = UserDocument(
            filename=file.filename,
            content=content[:2000],
            content_vector=vector
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        stored_files.append(doc)

    return stored_files
