from core.vector_backends.chroma_store import ChromaVectorStore
from uuid import uuid4
import os
import pytest
from core.utils.config import load_config

from core.registries.vector_registry import get_vector_db
from core.registries.embedding_registry import get_embedder
from core.registries.llm_registry import get_llm
from core.utils.prompt_loader import load_prompt_template

from core.llm_providers.openai_llm import OpenAIChatModel
from core.vector_backends.chroma_store import ChromaVectorStore
from core.embedding_models.openai_embedder import OpenAIEmbedder

openai_key = os.getenv("OPENAI_API_KEY")


@pytest.mark.skipif(not openai_key, reason="OpenAI key not found!!")
def test_add_and_retrieve():
  CONFIG = load_config()

  embedder = get_embedder(CONFIG["embedding"]["provider"])
  vector_store = get_vector_db(CONFIG["vector_store"]["provider"], embedder=embedder)
  vs = vector_store
  vs.add_message("user", "Artificial Intelligence is changing the world.")
  results = vs.get_top_k("What is changing the world?")
  assert results and "intelligence" in results[0].lower()
  print("✅ test_add_and_retrieve passed.")

""" @pytest.mark.skipif(not openai_key, reason="OpenAI key not found!!")
def test_vectorstore_basic():
  store = VectorStore()

  # Add messages
  documents = ["I love programming in Python", "Python is awesome", "We are using Vlite for vector store"]
  uuids = [str(uuid4()) for _ in range(len(documents))]

  store.add_documents(documents, "user", uuids)
  # Search
  results = store.search_similar("Tell me about Python", k=1)

  print("Search: ", results)
  print("All: ", store.list_all())

  store.update(str(uuids[-1]), "We switched vector store to Chroma", "user")
  print("Updated: ", store.list_all())


@pytest.mark.skipif(not openai_key, reason="OpenAI key not found!!")
def test_vectorstore_single():
  store = VectorStore()
  

  # Add message
  #store.add_message("I love programming in Python", "user")
  #store.add_message("Python is awesome", "assistant")
  temp_uuid = str(uuid4())
  store.add_message("We are using Chroma for vector store", "user")
  print("All: ", store.list_all())

if __name__ == "__main__":
  print(f"Executing from {sys.executable}")
  test_vectorstore_basic()
  #test_vectorstore_single() """