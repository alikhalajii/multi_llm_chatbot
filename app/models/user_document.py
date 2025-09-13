from sqlalchemy import Column, Integer, String, Text
from pgvector.sqlalchemy import Vector
from app.core.db import Base
import os

EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", "768"))


class UserDocument(Base):
    __tablename__ = "user_documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    content_vector = Column(Vector(EMBEDDING_DIM))
