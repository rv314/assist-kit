from core.guardrails.role_enforcer import RoleEnforcer
from core.guardrails.abuse_filter import AbuseFilter

class GuardManager:
  def __init__(self, config: dict):
    self.role_enforcer = RoleEnforcer(config)
    self.abuse_filter = AbuseFilter(config.get("guardrails", {}).get("abuse_filter", {}))

  def check_all(self, message: str) -> dict:
    # Default
    result = {
      "allowed": True,
      "violations": []
    }

    # Role Enforcer
    role_check = self.role_enforcer.enforce_scope(message)
    if not role_check["allowed"]:
      result["allowed"] = False
      result["violations"].append(role_check)

    # Abuse filtering
    abuse_result = self.abuse_filter.check(message)
    if not abuse_result:
      return abuse_result

    return result