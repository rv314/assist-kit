import re

class AbuseFilter:
  def __init__(self, config: dict = None):
    self.config = config or {}
    self.blocklist = set(self.config.get("blocklist", [])) or {
      "hate", "kill", "suicide", "drug abuse", "stupid", "racist"
    }
    self.regex_pattern = re.compile(r'\b(' + '|'.join(re.escape(word) for word in self.blocklist) + r')\b', re.IGNORECASE)

  
  def is_abusive(self, message: str) -> dict:
    """Returns true if abusive content is found."""
    return bool(self.regex_pattern.search(message))
  

  def check(self, message: str) -> dict:
    """Main check function returning decision and reason"""
    if self.is_abusive(message):
      return {
        "allowed": False,
        "reason": "Message contains abusive or inappropriate language."
      }
    return {"allowed": True}
