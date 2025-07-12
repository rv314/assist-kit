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
      if topic.lower() is user_input.lower():
        return False
      
    return True
