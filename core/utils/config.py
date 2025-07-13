import json
import os
import yaml

def load_config():
  base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  config_path = os.path.join(base_dir, "config/config.json")
  with open(config_path, "r") as f:
    return json.load(f)
  
def load_injection_rules():
  base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  rules_path = os.path.join(base_dir, "config/injection_rules.yaml")
  with open(rules_path, "r") as f:
      return yaml.safe_load(f)
  
if __name__ == "__main__":
  load_config()