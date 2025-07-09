import json
import os

def load_config():
  base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  config_path = os.path.join(base_dir, "config/config.json")
  with open(config_path, "r") as f:
    return json.load(f)
  
if __name__ == "__main__":
  load_config()