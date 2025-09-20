from pydantic import BaseModel
from typing import List, Dict


class ChatRequest(BaseModel):
    user_input: str
    history: List[Dict[str, str]] | None = None
    model_key: str


class ChatResponse(BaseModel):
    response: str
    history: List[Dict[str, str]]
