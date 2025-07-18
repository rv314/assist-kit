# assistant/orchestrator.py
from core.utils.token_limits import trim_messages
from typing import List, Dict
from core.utils.debug import debug_log, print_eval_log, print_vector_results
from core.utils.evaluation_logger import log_eval

from core.registries.vector_registry import get_vector_db
from core.registries.embedding_registry import get_embedder
from core.registries.llm_registry import get_llm
from core.utils.prompt_loader import load_prompt_template

from core.llm_providers.openai_llm import OpenAIChatModel
from core.engine.vector_store import VectorStore
from core.embedding_models.openai_embedder import OpenAIEmbedder

from abc import ABC, abstractmethod


class InteractionEngine(ABC):
  
  def __init__(self, config: dict, collection_name: str):
    self.model = config["llm"]["model"]
    self.max_tokens = config.get("max_tokens", 3000)
    self.debug = config.get("logging", {}).get("debug", False)

    # Register LLM via registry
    self.llm = get_llm(config["llm"]["provider"], config=config["llm"])

    # Register embedder and vector store
    embedder = get_embedder(config["embedding"]["provider"])
    self.vector_store = VectorStore(
      full_config=config, 
      collection_name=collection_name,
      embedder=embedder
    )
    
  
  @abstractmethod
  def run(self, messages: List[Dict[str, str]]) -> str:
    pass