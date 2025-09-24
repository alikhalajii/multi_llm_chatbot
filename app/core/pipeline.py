from typing import Dict, Any, List
import logging
from langdetect import detect as _detect

from app.core.adapters import get_chat_model
from app.llms import TOGETHER_MODEL_MAP, DEFAULT_MODELS
from app.core.db import get_db
from app.services.embedding_service import generate_embedding
from app.services.document_service import retrieve_relevant_docs

logger = logging.getLogger(__name__)


DEFAULT_TOGETHER_KEY = DEFAULT_MODELS["together"]
RELEVANCE_THRESHOLD = 0.65

FALLBACK_PHRASES = {
    "en": "No answer found in the loaded documents.",
    "de": "Keine Antwort in den geladenen Dokumenten gefunden.",
    "fa": "در اسناد بارگذاری‌شده پاسخی پیدا نشد.",
    "fr": "Aucune réponse trouvée dans les documents chargés.",
}


def detect_language_simple(text: str) -> str:
    try:
        return str(_detect(text))
    except Exception:
        return "en"


# Chat Pipeline
class SimpleChatApp:
    def __init__(self, provider: str, model_key: str | None = None):
        resolved_key: str = model_key if model_key else DEFAULT_TOGETHER_KEY
        model_id: str = TOGETHER_MODEL_MAP.get(resolved_key, resolved_key)
        logger.info(
            "🤖 Initializing SimpleChatApp with model: %s -> %s", resolved_key, model_id
        )
        self.llm = get_chat_model(provider, model_id)
        self.db = next(get_db())

    def invoke(
        self, state: Dict[str, Any], config: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:
        messages: List[Dict[str, str]] = state["messages"]
        user_query = state.get("user_input")
        if not user_query:
            raise ValueError("Missing user_input")

        query_vector = generate_embedding(user_query)
        docs, max_score = retrieve_relevant_docs(self.db, query_vector, top_k=3)

        # Log similarity check
        logger.info("[PIPELINE] User query: %s", user_query[:100])
        logger.info(
            "[PIPELINE] Retrieved %d docs, max_score=%.3f (threshold=%.2f)",
            len(docs),
            max_score,
            RELEVANCE_THRESHOLD,
        )

        # Detect language for fallback
        lang = detect_language_simple(user_query)
        fallback = FALLBACK_PHRASES.get(lang[:2], FALLBACK_PHRASES["en"])

        # if no sufficiently relevant docs, return polite fallback (no LLM call)
        if not docs or max_score < RELEVANCE_THRESHOLD:
            logger.info("[PIPELINE] Fallback triggered → responding with: %s", fallback)
            return {"messages": [{"role": "assistant", "content": fallback}]}

        # Else: strict grounding
        context_text = "\n\n".join([f"{d.filename}: {d.content}" for d in docs])
        system_msg = {
            "role": "system",
            "content": (
                "You are a polite, friendly assistant. ALWAYS respond in the same language as the user's last message. "
                "You MUST use ONLY the documents given below to answer. Do not use external knowledge. "
                "If the documents do not contain the answer, reply EXACTLY with: "
                "'No answer found in the loaded documents.' Do not add anything else."
                f"\n\nDocuments:\n{context_text}"
            ),
        }

        # Place system message immediately before last user message
        messages = messages[:-1] + [system_msg, messages[-1]]

        logger.info("[PIPELINE] Passing %d messages to LLM", len(messages))
        ai_msg = self.llm.invoke(messages)
        return {"messages": [ai_msg]}


def build_config(provider: str, model_key: str | None = None) -> Dict[str, Any]:
    """Build configuration for the chat app based on provider and model_key."""
    resolved_key: str = model_key if model_key else DEFAULT_TOGETHER_KEY
    return {"configurable": {"thread_id": "abc123"}, "model": resolved_key}


app = SimpleChatApp("together", DEFAULT_TOGETHER_KEY)
