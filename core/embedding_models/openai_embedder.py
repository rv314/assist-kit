from langchain_community.embeddings import OpenAIEmbeddings
from core.registries.embedding_registry import register_embedder
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@register_embedder("openai")
class OpenAIEmbedder(OpenAIEmbeddings):
  def __init__(self, **kwargs):
    super().__init__(openai_api_key=os.getenv("OPENAI_API_KEY"), **kwargs)

  
  def embed_query(self, text: str) -> list[float]:
    """
    Overriding to ensure it returns clean list of floats.
    """
    embedding = super().embed_query(text)
    logger.debug(f"Embedding for text: '{text[:30]} ....' -> type: {type(embedding)}, len: {len(embedding)}")
    if isinstance(embedding, tuple):
      embedding = embedding[0]
    return list(embedding)