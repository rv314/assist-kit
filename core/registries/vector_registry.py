VECTOR_DB_REGISTRY = {}

def register_vector_db(name):
  """Decorator to register a vector DB implementation"""
  def wrapper(cls):
    VECTOR_DB_REGISTRY[name] = cls
    return cls
  return wrapper


def get_vector_db(name, **kwargs):
  """Retrieve a vector DB class by name."""
  if name not in VECTOR_DB_REGISTRY:
    raise ValueError(f"Vector DB '{name}' is not registered.")
  return VECTOR_DB_REGISTRY[name](**kwargs)
