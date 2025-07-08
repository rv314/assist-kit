import yaml
from pathlib import Path

def load_prompt_template(path: str = "src/llm/prompt.yaml") -> str:
  with open(Path(path), "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)
  return config.get("system_prompt", "")