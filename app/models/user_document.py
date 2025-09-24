import os
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from pgvector.sqlalchemy import Vector

EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", "768"))


class Base(DeclarativeBase):
    pass


class UserDocument(Base):
    __tablename__ = "user_documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    content_vector: Mapped[list[float]] = mapped_column(
        Vector(EMBEDDING_DIM), nullable=False
    )

    def __repr__(self) -> str:
        return f"<UserDocument(id={self.id}, filename='{self.filename}')>"
