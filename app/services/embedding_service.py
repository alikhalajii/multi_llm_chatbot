import os
from typing import List
from langchain_together import TogetherEmbeddings
from app.config import get_api_key

EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", "768"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "togethercomputer/m2-bert-80M-8k-retrieval")

_embeddings = TogetherEmbeddings(
    model=EMBEDDING_MODEL,
    api_key=get_api_key("TOGETHER_API_KEY", "Enter your Together API key")
)


def generate_embedding(text: str) -> List[float]:
    vec = _embeddings.embed_query(text)
    if len(vec) < EMBEDDING_DIM:
        vec = vec + [0.0] * (EMBEDDING_DIM - len(vec))
    elif len(vec) > EMBEDDING_DIM:
        vec = vec[:EMBEDDING_DIM]
    return vec
