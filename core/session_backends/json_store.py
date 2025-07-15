import json
from pathlib import Path
from datetime import datetime
from core.registries.session_registry import register_session_backend


@register_session_backend("json")
class JSONSessionStore:
  def __init__(self, config=None):
    config = config or {}
    self.file_path = Path(config.get("json_path", "session_data/session_data.json"))
    self.file_path.parent.mkdir(parents=True, exist_ok=True)
    if not self.file_path.exists():
      self._write({})


  def _read(self):
    with open(self.file_path, "r", encoding="utf-8") as f:
      return json.load(f)
    
  
  def _write(self, data):
    with open(self.file_path, "w", encoding="utf-8") as f:
      json.dump(data, f, indent=2)

  
  def load_session(self, session_id: str) -> list:
    data = self._read()
    return data.get(str(session_id), [])
  

  def save_session(self, session_id: str, messages: list):
    data = self._read()
    data[str(session_id)] = messages
    self._write(data)


  def clear_session(self, session_id: str):
    data = self._read()
    if session_id in data:
      del data[str(session_id)]
      self._write(data)