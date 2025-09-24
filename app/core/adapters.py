from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_mistralai import ChatMistralAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEndpoint
from langchain_together import ChatTogether
from typing import Any, Optional
from pydantic import SecretStr

from app.config import get_api_key
from app.llms import DEFAULT_MODELS, TOGETHER_MODEL_MAP, DEFAULT_PARAMS


def get_chat_model(
    provider: str, model_key: Optional[str] = None, **kwargs: Any
) -> Any:
    """
    Return a chat model instance for the given provider and model.

    Args:
        provider (str): Name of the provider ("openai", "anthropic", "mistral",
                        "gemini", "huggingface", "together").
        model_key (str | None): Model identifier. If None, a default will be used.
        **kwargs: Extra model parameters (overrides DEFAULT_PARAMS).

    Returns:
        LangChain Chat instance.
    """
    params = {**DEFAULT_PARAMS, **kwargs}
    provider = provider.lower()

    if provider == "openai":
        return ChatOpenAI(
            model=model_key or DEFAULT_MODELS["openai"],
            api_key=SecretStr(get_api_key("OPENAI_API_KEY")),
            **params,
        )

    elif provider == "anthropic":
        return ChatAnthropic(
            model_name=model_key or DEFAULT_MODELS["anthropic"],
            api_key=SecretStr(get_api_key("ANTHROPIC_API_KEY")),
            **params,
        )

    elif provider == "mistral":
        return ChatMistralAI(
            model_name=model_key or DEFAULT_MODELS["mistral"],
            api_key=SecretStr(get_api_key("MISTRAL_API_KEY")),
            **params,
        )

    elif provider == "gemini":
        return ChatGoogleGenerativeAI(
            model=model_key or DEFAULT_MODELS["gemini"],
            google_api_key=get_api_key("GOOGLE_API_KEY"),
            **params,
        )

    elif provider == "huggingface":
        return HuggingFaceEndpoint(
            repo_id=model_key or DEFAULT_MODELS["huggingface"],
            task="text-generation",
            huggingfacehub_api_token=get_api_key("HUGGINGFACE_API_KEY"),
            **params,
        )

    elif provider == "together":
        # Map friendly key to Together model id
        model_id = TOGETHER_MODEL_MAP.get(model_key or "", model_key or "")

        if not model_id:
            raise ValueError(f"Invalid TogetherAI model key: {model_key}")
        return ChatTogether(
            model=model_id, api_key=SecretStr(get_api_key("TOGETHER_API_KEY")), **params
        )

    else:
        raise ValueError(f"Unknown provider: {provider}")
