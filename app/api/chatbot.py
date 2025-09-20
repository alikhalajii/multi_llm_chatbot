from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any, List, Dict

from app.core.db import get_db
from app.core.pipeline import SimpleChatApp
from app.schemas.chat import ChatRequest, ChatResponse
from app.llms import TOGETHER_MODEL_MAP

router = APIRouter(tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest, db: Session = Depends(get_db)):
    if req.model_key not in TOGETHER_MODEL_MAP:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid model_key '{req.model_key}'. "
                   f"Allowed values: {list(TOGETHER_MODEL_MAP.keys())}"
        )

    if not req.user_input.strip():
        return ChatResponse(
            response=f"Hello! I'm {req.model_key}. How can I help you today?",
            history=req.history or []
        )

    # Rebuild conversation history
    messages: List[Dict[str, str]] = req.history.copy() if req.history else []

    # Add latest user query
    messages.append({"role": "user", "content": req.user_input})

    # Run pipeline (retrieval + LLM)
    chat_app = SimpleChatApp("together", req.model_key)
    try:
        result = chat_app.invoke({"messages": messages, "user_input": req.user_input})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model invocation failed: {str(e)}")

    ai_msg: Any = result["messages"][0]
    reply = ai_msg.content if hasattr(ai_msg, "content") else str(ai_msg)

    # Add assistant reply to history
    messages.append({"role": "assistant", "content": reply})

    return ChatResponse(response=reply, history=messages)
