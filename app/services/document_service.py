from sqlalchemy.orm import Session
from sqlalchemy import text
import logging

from app.models.user_document import UserDocument
from app.services.embedding_service import generate_embedding

logger = logging.getLogger(__name__)


def retrieve_relevant_docs(db: Session, query_vector: list[float], top_k: int = 3):
    """Retrieve top-k most relevant docs using Postgres ANN search (<-> operator)."""
    vector_str = "[" + ",".join(f"{x:.6f}" for x in query_vector) + "]"

    sql = text("""
        SELECT id, filename, content, content_vector,
               1 - (content_vector <-> CAST(:vec AS vector)) AS similarity
        FROM user_documents
        ORDER BY content_vector <-> CAST(:vec AS vector)
        LIMIT :k
    """)

    rows = db.execute(sql, {"vec": vector_str, "k": top_k}).mappings().all()

    docs, scores = [], []
    for row in rows:
        doc = UserDocument(
            id=row["id"],
            filename=row["filename"],
            content=row["content"],
            content_vector=row["content_vector"],
        )
        docs.append(doc)
        scores.append(row["similarity"])

        logger.info("[RETRIEVAL] Doc=%s similarity=%.3f snippet=%s",
                    row["filename"], row["similarity"], (row["content"] or "")[:120])

    max_score = max(scores) if scores else 0.0
    return docs, max_score


def store_document_with_embedding(db: Session, filename: str, content: str):
    """Store a document in DB with embedding."""
    logger.info("[STORE] Saving file=%s with %d characters", filename, len(content))

    vector = generate_embedding(content)
    logger.info("[STORE] Generated embedding length=%d", len(vector))

    doc = UserDocument(filename=filename, content=content, content_vector=vector)
    db.add(doc)
    db.commit()
    db.refresh(doc)

    logger.info("[STORE] Stored document id=%s filename=%s", doc.id, doc.filename)
    return doc
