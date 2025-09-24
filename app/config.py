import os
from dotenv import load_dotenv

load_dotenv()


def get_api_key(env_var: str, prompt: str | None = None) -> str:
    """Retrieve API key from environment variables."""
    value = os.getenv(env_var)
    if not value:
        raise ValueError(
            f"❌ Missing {env_var}. Please set it in your environment or .env file."
        )
    return value
