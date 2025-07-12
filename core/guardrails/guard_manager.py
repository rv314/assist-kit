from core.guardrails.role_enforcer import RoleEnforcer
from core.guardrails.abuse_filter import AbuseFilter
from core.guardrails.rate_limiter import RateLimiter
from core.guardrails.injection_detector import InjectionDetector

class GuardManager:
  def __init__(self, config: dict):
    self.role_enforcer = RoleEnforcer(config)
    self.abuse_filter = AbuseFilter(config.get("guardrails", {}).get("abuse_filter", {}))
    self.rate_limiter = RateLimiter(config.get("guardrails", {}).get("rate_limiter", {}))
    self.injection_detector = InjectionDetector(config.get("guardrails", {}).get("enable_injection_detector", True))

  def check_all(self, message: str, session_id: str) -> dict:
    
    # Role Enforcer
    role_result = self.role_enforcer.check(message)
    if not role_result["allowed"]:
      return role_result

    # Abuse filtering
    abuse_result = self.abuse_filter.check(message)
    if not abuse_result:
      return abuse_result
    
    # Rate limiter
    rate_limiter_result = self.rate_limiter.is_allowed(session_id)
    if not rate_limiter_result["allowed"]:
      return rate_limiter_result
    
    # Prompt injection detector
    injection_result = self.injection_detector.check(message)
    if not injection_result["allowed"]:
      return injection_result

    return {"allowed": True}
  

  def guard_results_handler(self, result: dict) -> str:
    """Returns user-fiendly explanation of denied prompts."""
    reason = result.get("reason", "unknown")
    details = result.get("details", "")

    # Predefined friendly message based on reasons
    reason_map = {
      "scope_violation": "🚫 This question is not allowed based on the assistant's current role.",
      "abuse_detected": "⚠️ Please avoid abusive or offensive language.",
      "prompt_injection": "⚠️ Suspicious input detected. Please rephrase your query.",
      "rate_limited": "⏳ You're sending messages too quickly. Please wait a moment.",
      "unknown": "⚠️ Your input was blocked due to an unspecified policy."
    }

    return reason_map.get(reason, reason_map["unknown"]) + (f"\n\n[Details: {details}]" if details else "")