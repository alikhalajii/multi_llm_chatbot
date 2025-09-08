from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_mistralai import ChatMistralAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEndpoint
from langchain_together import ChatTogether
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.config import get_api_key
from app.models import DEFAULT_MODELS, TOGETHER_MODEL_MAP, DEFAULT_PARAMS


def get_chat_model(provider: str, model: str | None = None, chain: bool = False, **kwargs):
    params = {**DEFAULT_PARAMS, **kwargs}
    provider = provider.lower()

    if provider == "openai":
        llm = ChatOpenAI(model=model or DEFAULT_MODELS["openai"],
                         api_key=get_api_key("OPENAI_API_KEY", "Enter your OpenAI API key"),
                         **params)
    elif provider == "anthropic":
        llm = ChatAnthropic(model=model or DEFAULT_MODELS["anthropic"],
                            api_key=get_api_key("ANTHROPIC_API_KEY", "Enter your Anthropic API key"),
                            **params)
    elif provider == "mistral":
        llm = ChatMistralAI(model=model or DEFAULT_MODELS["mistral"],
                            api_key=get_api_key("MISTRAL_API_KEY", "Enter your Mistral API key"),
                            **params)
    elif provider == "gemini":
        llm = ChatGoogleGenerativeAI(model=model or DEFAULT_MODELS["gemini"],
                                     google_api_key=get_api_key("GOOGLE_API_KEY", "Enter your Google API key"),
                                     **params)
    elif provider == "huggingface":
        llm = HuggingFaceEndpoint(repo_id=model or DEFAULT_MODELS["huggingface"],
                                  task="text-generation",
                                  huggingfacehub_api_token=get_api_key("HUGGINGFACE_API_KEY", "Enter your HuggingFace token"),
                                  **params)
    elif provider == "together":
        model_id = TOGETHER_MODEL_MAP.get(model, model)
        if not model_id:
            raise ValueError("Invalid Together model id.")
        llm = ChatTogether(model=model_id,
                           api_key=get_api_key("TOGETHER_API_KEY", "Enter your Together API key"),
                           **params)
    else:
        raise ValueError(f"Unknown provider: {provider}")

    if chain:
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Keep answers short."),
            ("human", "{input}")
        ])
        return prompt | llm | StrOutputParser()

    return llm
