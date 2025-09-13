from pydantic import BaseModel
from typing import Optional


class DocumentBase(BaseModel):
    filename: str
    preview: Optional[str] = None
    vector_len: int = 0


class DocumentOut(DocumentBase):
    id: int

    class Config:
        from_attributes = True
