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
    abusive_word = self.regex_pattern.search(message)
    return (bool(self.regex_pattern.search(message)), abusive_word)
  

  def check(self, message: str) -> dict:
    """Main check function returning decision and reason"""
    is_abusive, abusive_word = self.is_abusive(message)
    if is_abusive:
      return {
        "allowed": False,
        "reason": "abuse_detected",
        "details": f"Message contains abusive or inappropriate language: '{abusive_word}'."
      }
    return {"allowed": True}
