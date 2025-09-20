from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.user_document import UserDocument

SIMILARITY_THRESHOLD = 0.7  


def retrieve_similar_docs(db: Session, query_vec, top_k: int = 3):
    """ Retrieve similar documents based on the query vector. """
    stmt = (
        select(
            UserDocument,
            UserDocument.content_vector.cosine_distance(query_vec).label("dist")
        )
        .order_by(UserDocument.content_vector.cosine_distance(query_vec))
        .limit(top_k)
    )
    rows = db.execute(stmt).all()

    docs = [row[0] for row in rows if row[1] <= SIMILARITY_THRESHOLD]
    return docs
