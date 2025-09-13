from pydantic import BaseModel
from typing import List, Dict, Literal
from app.llms import DEFAULT_MODELS


class ChatRequest(BaseModel):
    user_input: str
    model_key: str = DEFAULT_MODELS["together"]
    history: List[Dict[str, str]] = []


class ChatResponse(BaseModel):
    response: str
