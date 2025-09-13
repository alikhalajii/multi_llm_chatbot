import os

DEFAULT_MODELS = {
    "openai": "gpt-4o-mini",
    "anthropic": "claude-3-5-sonnet-20240620",
    "mistral": "mistral-medium",
    "gemini": "gemini-1.5-flash",
    "huggingface": "deepseek-ai/DeepSeek-R1-0528",
    "together": "meta_llama_3.1_8b"

}

TOGETHER_MODEL_MAP = {
    "deepseek_r1_0528": "deepseek-ai/DeepSeek-R1-0528-tput",
    "google_gemma_3n_4b": "google/gemma-3n-E4B-it",  # $0.04
    "meta_llama_3.1_8b": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",  # $0.18
    "openai_gpt_oss_20b": "openai/gpt-oss-20b",  # $0.20
    "mistral_7b_v0.2": "mistralai/Mistral-7B-Instruct-v0.2",  # $0.20
    "qwen_2.5_7b_turbo": "Qwen/Qwen2.5-7B-Instruct-Turbo",  # $0.30
    "meta_llama_3.3_70b": "meta-llama/Llama-3.3-70B-Instruct-Turbo",  # $0.88
    "qwen_2.5_72b": "Qwen/Qwen2.5-72B-Instruct-Turbo"  # $1.20
}

DEFAULT_PARAMS = {
    "max_tokens": 200,
    "temperature": 0.5,
}


TOGETHER_DEFAULT = os.getenv("TOGETHER_DEFAULT_MODEL", "Llama_3.1_8B")
