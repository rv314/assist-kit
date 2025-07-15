from core.registries.session_registry import get_session_backend
from core.session_backends.json_store import JSONSessionStore


class SessionManager:
  def __init__(self, full_config):
    session_store_config = full_config.get("session_store", {})
    session_store_backend_name = session_store_config.get("provider", "json")
    session_store_backend_config = session_store_config.get("config", {})
    self.store = get_session_backend(session_store_backend_name, config=session_store_backend_config)


  def load_session(self, session_id: str) -> list:
    return self.store.load_session(session_id)
  

  def save_session(self, session_id: str, messages: list):
    self.store.save_session(session_id, messages)


  def clear_session(self, session_id: str):
    self.store.clear_session(session_id)