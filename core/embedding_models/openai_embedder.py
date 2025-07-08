from langchain_community.embeddings import OpenAIEmbeddings
from registries.embedding_registry import register_embedder
import os

@register_embedder("openai")
class OpenAIEmbedder(OpenAIEmbeddings):
  def __init__(self, **kwargs):
    super().__init__(openai_api_key=os.getenv("OPENAI_API_KEY"), **kwargs)