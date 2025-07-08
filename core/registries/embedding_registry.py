from typing import Callable, Dict

_EMBEDDING_REGISTRY: Dict[str, Callable] = {}

def register_embedder(name: str):
  def wrapper(cls):
    _EMBEDDING_REGISTRY[name] = cls
    return cls
  return wrapper


def get_embedder(name: str, **kwargs):
  if name not in _EMBEDDING_REGISTRY:
    print(f"{_EMBEDDING_REGISTRY} is the registry")
    raise ValueError(f"Embedder '{name}' is not registered.")
  return _EMBEDDING_REGISTRY[name](**kwargs)