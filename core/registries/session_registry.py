from typing import Callable

_SESSION_REGISTRY = {}

def register_session_backend(name: str):
  def wrapper(cls: Callable):
    _SESSION_REGISTRY[name] = cls
    return cls
  return wrapper


def get_session_backend(name: str, **kwargs):
  if name not in _SESSION_REGISTRY:
    raise ValueError(f"Session backend '{name}' not registered.")
  return _SESSION_REGISTRY[name](**kwargs)