LLM_REGISTRY = {}

def register_llm(name):
  def wrapper(cls):
    LLM_REGISTRY[name] = cls
    return cls
  return wrapper


def get_llm(name: str, config: dict = None):
  if name not in LLM_REGISTRY:
    raise ValueError(f"LLM provider '{name}' not registered.")
  return LLM_REGISTRY[name](config = config or {})