class RoleEnforcer:
  def __init__(self, config):
    self.scope = config.get("llm").get("scope", "general")
    self.guard_config = config.get("guardrails", {}).get("role_definitions", {})
    self.enforce_scope = config.get("guardrails", {}).get("enforce_scope", True)

  
  def is_in_scope(self, user_input: str) -> bool:
    if not self.enforce_scope or self.scope == "general":
      return True
    
    role_rules = self.guard_config.get(self.scope, {})
    blocked = role_rules.get("blocked_topics", [])

    for topic in blocked:
      if topic.lower() in user_input.lower(): # Replace with NLP-based matching (embedding similarity)
        return False
      
    return True
  

  def check(self, user_input: str) -> dict:
    if self.is_in_scope(user_input):
      return {"allowed": True}
    return {
      "allowed": False,
      "reason": "scope_violation",
      "details": f"Input not allowed in current scope: '{self.scope}'."
    }
