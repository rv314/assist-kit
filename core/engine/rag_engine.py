from core.utils.pdf_loader import extract_pdf_text
from core.engine.orchestrator import InteractionEngine
from typing import List


class RAGEngine(InteractionEngine):
  def __init__(self, config: dict, collection_name: str = "rag_docs"):
    super().__init__(config=config, collection_name=collection_name)


  def ingest_pdf(self, file_path: str) -> List[str]:
    """Extracts text chunks from PDF and strores embeddings in vector DB."""
    docs = extract_pdf_text(file_path)
    texts = [doc["text"] for doc in docs]
    metadata = [doc["metadata"] for doc in docs]
    self.vector_store.add_documents(texts, metadata)

    return texts
  

  def query(self, user_input: str, top_k: int = 3) -> str:
    """Perform Retrieval augmented generation: 
        1. Search vector DB
        2. Build prompt
        3. Generate answer
    """
    results = self.vector_store.similarity_search(user_input, top_k=top_k)
    retrieved_texts = [doc.page_content for doc in results]

    context = "\n\n".join(retrieved_texts)
    prompt = f"Answer the question based on following content:\n\n{context}\n\nQuestion: {user_input}"

    response = self.llm(prompt)
    return response
