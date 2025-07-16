from core.registries.vector_registry import get_vector_db
from core.vector_backends.chroma_store import ChromaVectorStore


class VectorStore:
  def __init__(self, full_config: dict, collection_name: str = "chat_logs", embedder=None):
    vector_store_config = full_config.get("vector_store", {})
    vector_store_backend_name = vector_store_config.get("provider", "chroma")
    vector_store_backend_config = vector_store_config.get("config", "")
    
    self.store = get_vector_db(
      vector_store_backend_name, 
      config=vector_store_backend_config,
      embedder=embedder,
      collection_name=collection_name
      )

  
  def add_documents(self, chunks: list):
    """Add list of documents to vector DB"""
    return self.store.add_documents(chunks)
  

  def similarity_search(self, query: str, top_k: int = 5):
    """Run similarity search over vector DB."""
    return self.store.similarity_search(query, top_k=top_k)
  

  def log_chat_qa(self, question: str, answer: str):
    """Purely for chat session to log / store data in Q & A format"""
    return self.store.log_chat_qa(question, answer)


  def clear(self):
    """Clear all vectors"""
    return self.store.clear()