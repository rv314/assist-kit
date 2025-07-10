from core.registries.session_registry import get_session_backend
from core.session_backends.json_store import JSONSessionStore


class SessionManager:
  def __init__(self, config):
    backend_name = config.get("session_store", {}).get("provider", "json")
    backend_config = config.get("session_store", {}).get("config", {})
    self.store = get_session_backend(backend_name, config=backend_config)


  def load_session(self, session_id: str) -> list:
    return self.store.load_session(session_id)
  

  def save_session(self, session_id: str, messages: list):
    self.store.save_session(session_id, messages)


  def clear_session(self, session_id: str):
    self.store.clear_session(session_id)