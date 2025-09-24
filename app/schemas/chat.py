from pydantic import BaseModel
from typing import List, Dict

from app.llms import TOGETHER_DEFAULT


class ChatRequest(BaseModel):
    user_input: str
    history: List[Dict[str, str]] | None = None
    model_key: str = TOGETHER_DEFAULT


class ChatResponse(BaseModel):
    response: str
    history: List[Dict[str, str]]
