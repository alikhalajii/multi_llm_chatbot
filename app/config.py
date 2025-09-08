import os
import getpass
from dotenv import load_dotenv

load_dotenv()


def get_api_key(env_var: str, prompt: str) -> str:
    """Get API key from environment variable or prompt the user."""
    key = os.getenv(env_var)
    if not key:
        key = getpass.getpass(f"{prompt}: ")
        os.environ[env_var] = key
    return key
