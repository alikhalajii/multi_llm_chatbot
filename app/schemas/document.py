from pydantic import BaseModel


class DocumentOut(BaseModel):
    id: int
    filename: str
    content_preview: str
    vector_len: int

    class Config:
        from_attributes = True
