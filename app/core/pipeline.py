from typing import Dict, Any, List
from langchain_core.messages import BaseMessage
from app.core.adapters import get_chat_model
from app.llms import TOGETHER_MODEL_MAP, DEFAULT_MODELS

DEFAULT_TOGETHER_KEY = DEFAULT_MODELS["together"]


class SimpleChatApp:
    def __init__(self, provider: str, model_key: str | None = None):
        resolved_key: str = model_key if model_key else DEFAULT_TOGETHER_KEY
        model_id: str = TOGETHER_MODEL_MAP.get(resolved_key, resolved_key)
        print(f"🤖 Initializing SimpleChatApp with model: {resolved_key} -> {model_id}")
        self.llm = get_chat_model(provider, model_id)

    def invoke(self, state: Dict[str, Any], config: Dict[str, Any] | None = None) -> Dict[str, List[BaseMessage]]:
        messages: List[BaseMessage] = state["messages"]
        ai_msg = self.llm.invoke(messages)
        return {"messages": [ai_msg]}


def build_config(provider: str, model_key: str | None = None) -> Dict[str, Any]:
    """ Build a configuration dictionary for initializing SimpleChatApp. """
    resolved_key: str = model_key if model_key else DEFAULT_TOGETHER_KEY
    return {"configurable": {"thread_id": "abc123"}, "model": resolved_key}


# Initialize a default SimpleChatApp instance with Together model
app = SimpleChatApp("together", DEFAULT_TOGETHER_KEY)
