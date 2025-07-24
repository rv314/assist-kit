from chromadb import PersistentClient
from chromadb.config import Settings
from pathlib import Path
from core.registries.vector_registry import register_vector_db
from core.utils.config import load_config


@register_vector_db("chroma")
class ChromaVectorStore():
  def __init__(self, config: dict = None, embedder = None, collection_name: str = "assist-kit"):
    if embedder is None:
      raise ValueError("Embedder must be provided for vector store.")
    self.embedder = embedder

    # Load config if not passed.
    config = config or load_config()
    vector_config = config.get("vector_store", {})

    # Get persistent path from config or fallback
    persist_path = vector_config.get("persist_directory", "vectors/chroma")
    Path(persist_path).mkdir(parents=True, exist_ok=True)

    # Initialize Chroma client
    self.client = PersistentClient(path=str(persist_path))
    self.collection_name = collection_name
    self.collection = self.client.get_or_create_collection(name=collection_name)


  # Add documents function: Used by RAG pipeline
  def add_documents(self, chunks: list[dict]):
    """
    Accepts list of chunks: 
    [{"id:" ....,
      "text": ...,
      "metadata": {...}}, ...]
    """
    print(f"Received Text: {chunks}")
    ids = [chunk["id"] for chunk in chunks]
    texts = [chunk["text"] for chunk in chunks]
    embeddings = []
    for text in texts:
      emb = self.embedder.embed_query(text)
      embeddings.append(emb)
    metadatas = [chunk.get("metadata", {}) for chunk in chunks]

    self.collection.add(documents=texts, ids=ids, embeddings=embeddings, metadatas=metadatas)

    # TODO: Below code is a bug, needs investigation to fix
    """
    Can be format issue, also its better to have deduplication done using text-based hashing
    instead of id-based
    """
    """ # Remove duplicates
    existing_ids = self.collection.get(include=["documents"]).get("ids", [])
    new_chucks = [(i, t, e, m) for i, t, e, m in zip(ids, texts, embeddings, metadatas) if i not in existing_ids]

    if new_chucks:
       ids, texts, embeddings, metadatas = zip(*new_chucks)
       self.collection.add(documents=texts, ids=ids, embeddings=embeddings, metadatas=metadatas) """

  
  def similarity_search(self, query: str, top_k: int = 3, similarity_threshold: float = 0.3):
    embedding = self.embedder.embed_query(query)
    results = self.collection.query(
      query_embeddings=[embedding], 
      n_results=top_k,
      include=["documents", "distances", "metadatas"]
      )
    
    documents = results.get("documents", [[]])[0]
    distances = results.get("distances", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    return [
      {
        "text": doc,
        "score": dist,
        "metadata": meta
      }
      for doc, dist, meta in zip(documents, distances, metadatas)
      if dist <= similarity_threshold
    ]
  

  def clear(self):
    self.client.delete_collection(self.collection_name)
    self.collection = self.client.get_or_create_collection(name=self.collection_name)

  
  def log_chat_qa(self, question: str, answer: str):
    """Purely for chat session to log / store data in Q & A format"""
    entry = f"Q: {question}\nA: {answer}"
    entry_id = f"user_{hash(entry)}"

    # Check for existing id to prevent duplicates
    existing_ids = self.collection.get(include=["documents"]).get("ids", [])
    if entry_id in existing_ids:
      return
    
    embeddings = self.embedder.embed_query(entry)
    self.collection.add(
      documents=[entry],
      embeddings=[embeddings],
      ids=[entry_id],
      metadatas=[{"source": "chat_log"}]
    )
  

  def add_message(self, question: str, answer: str):
    """Embed and store Q&A pair into Chroma vector DB."""
    # content = f"Q: {question.strip()}\nA: {answer.strip()}"
    entry = f"Q: {question}\nA: {answer}"
    entry_id = f"user_{hash(entry)}"

    # Check for existing id to prevent duplicates
    existing = self.collection.get(include=["documents"])
    existing_ids = existing.get("ids", [])
    if entry_id in existing_ids:
      return
    
    embeddings = self.embedder.embed_query(entry)
    self.collection.add(
      documents=[entry],
      embeddings=[embeddings],
      ids=[entry_id]
    )
    # print(f"🧠 Added to vector store:\n{content[:100]}...\n")

  def get_top_k(self, query: str, k: int = 3, similarity_threshold: float = 0.3) -> list[tuple[str, float]]:
    """Retrieve top-k similar Q&A messages from vector DB."""
    embeddings = self.embedder.embed_query(query)

    results = self.collection.query(
        query_embeddings=[embeddings],
        n_results=k,
        include=["documents", "distances"]
    )

    documents = results.get("documents", [[]])[0]
    distances = results.get("distances", [[]])[0]

    filtered = [
        (doc, dist)
        for doc, dist in zip(documents, distances)
        if dist <= similarity_threshold
    ]

    return filtered
  
