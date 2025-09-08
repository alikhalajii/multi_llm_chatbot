DEFAULT_MODELS = {
    "openai": "gpt-4o-mini",
    "anthropic": "claude-3-5-sonnet-20240620",
    "mistral": "mistral-medium",
    "gemini": "gemini-1.5-flash",
    "huggingface": "deepseek-ai/DeepSeek-R1-0528",
}

TOGETHER_MODEL_MAP = {
    "deepseek_r1_70b": "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
    "llama_3_70b": "meta-llama/Llama-3-70b-chat-hf",
    "qwen_1.5_72b": "Qwen/Qwen1.5-72B-Chat",
    "llama_3_8b": "meta-llama/Meta-Llama-3-8B-Instruct-Lite",
    "gpt_oss_20b": "openai/gpt-oss-20b",
    "mistral_7b": "mistralai/Mistral-7B-Instruct-v0.2",
}

DEFAULT_PARAMS = {
    "max_tokens": 200,
    "temperature": 0.5,
}
