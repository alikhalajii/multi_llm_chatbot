from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any, List, Dict

from app.core.db import get_db
from app.services.embedding_service import generate_embedding
from app.services.retrieval_service import retrieve_similar_docs
from app.core.pipeline import SimpleChatApp
from app.schemas.chat import ChatRequest, ChatResponse
from app.llms import TOGETHER_MODEL_MAP, DEFAULT_MODELS

router = APIRouter(tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest, db: Session = Depends(get_db)):
    # Validate model key
    if req.model_key not in TOGETHER_MODEL_MAP:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid model_key '{req.model_key}'. "
                   f"Allowed values: {list(TOGETHER_MODEL_MAP.keys())}"
        )

    # Handle empty input
    if not req.user_input.strip():
        return ChatResponse(
            response=f"Hello! I'm {req.model_key}. How can I help you today?"
        )

    query_vec = generate_embedding(req.user_input)
    docs = retrieve_similar_docs(db, query_vec, top_k=3)

    context = "\n\n".join(d.content or "" for d in docs) if docs else ""

    messages: List[Dict[str, str]] = req.history.copy() if req.history else []

    if context:
        system_content = (
            f"You are a polite, document-grounded assistant. "
            f"Your name is {req.model_key}. "
            "Always reply in the same language the user speaks (English, German, Farsi, or French). "
            "Keep responses short, clear, and respectful. "
            "Answer only using the following uploaded documents:\n\n"
            f"{context}\n\n"
            "If the question is partially related but unclear, ask politely for clarification. "
            "If unrelated to the documents, suggest: 'Please upload a relevant document so I can assist you.' "
            "If the documents don’t contain the answer, reply exactly: 'No answer found in the loaded documents.' "
        )
    else:
        system_content = (
            f"You are a polite, document-grounded assistant. "
            f"Your name is {req.model_key}. "
            "Always reply in the same language the user speaks (English, German, Farsi, or French). "
            "Keep responses short, clear, and respectful."
            "Since no documents are uploaded, you cannot answer any question, including factual, commonsense, or math questions. "
            "If asked, reply exactly: 'No answer found in the loaded documents.' "
            "You may also suggest: 'Please upload a relevant document so I can assist you.' "
        )

    messages.insert(0, {"role": "system", "content": system_content})

    # Resolve friendly key → Together model id
    resolved_key: str = req.model_key if req.model_key is not None else DEFAULT_MODELS["together"]
    model_id: str = TOGETHER_MODEL_MAP.get(resolved_key, resolved_key)

    print(f"✅ Using model: {resolved_key} -> {model_id}")

    chat_app = SimpleChatApp("together", model_id)

    try:
        result = chat_app.invoke({"messages": messages})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model invocation failed: {str(e)}")

    ai_msg: Any = result["messages"][0]
    reply = ai_msg.content if hasattr(ai_msg, "content") else str(ai_msg)

    messages.append({"role": "assistant", "content": reply})

    return ChatResponse(response=reply)
