import yaml
import re

class InjectionDetector:
  def __init__(self, config=None, rules_path='config/injection_rules.yaml'):
    self.enabled = config.get("guardrails", {}).get("enable_injection_detector", True)
    with open(rules_path, "r") as f:
      rules = yaml.safe_load(f)
    self.suspicious_patterns = rules.get("injection_detector", {}).get("suspicious_patterns", [])


  def is_safe(self, user_input: str) -> bool:
    if not self.enabled:
      return True
    
    for pattern in self.suspicious_patterns:
      if re.search(pattern, user_input):
        return (False, pattern)
    return True
  

  def check(self, user_input: str) -> dict:
    is_safe, pattern = self.is_safe(user_input)
    if is_safe:
      return {"allowed": True}
    return {
      "allowed": False,
      "reaons": "prompt_injection",
      "details": f"Detected suspicious pattern: '{pattern}'."
    }