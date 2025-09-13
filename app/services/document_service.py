from sqlalchemy.orm import Session
from sqlalchemy import func
import numpy as np

from app.models.user_document import UserDocument
from app.services.embedding_service import generate_embedding


def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
        return 0.0
    return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))


def retrieve_relevant_docs(db: Session, query_vector: list, top_k: int = 3):
    docs = db.query(UserDocument).all()
    scored_docs = []
    for doc in docs:
        score = cosine_similarity(query_vector, doc.content_vector)
        scored_docs.append((score, doc))
    scored_docs.sort(key=lambda x: x[0], reverse=True)
    top_docs = [doc for score, doc in scored_docs[:top_k]]
    return top_docs


def store_document_with_embedding(db, filename: str, content: str):
    vector = generate_embedding(content)
    from app.models.user_document import UserDocument
    doc = UserDocument(filename=filename, content_vector=vector)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc