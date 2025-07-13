from core.guardrails.role_enforcer import RoleEnforcer
from core.guardrails.abuse_filter import AbuseFilter
from core.guardrails.rate_limiter import RateLimiter
from core.guardrails.injection_detector import InjectionDetector

class GuardManager:
  def __init__(self, config: dict):
    self.role_enforcer = RoleEnforcer(config)
    self.abuse_filter = AbuseFilter(config.get("guardrails", {}).get("abuse_filter", {}))
    self.rate_limiter = RateLimiter(config.get("guardrails", {}).get("rate_limiter", {}))
    self.injection_detector = InjectionDetector(config.get("guardrails", {}))

  def get_all_guard_results(self, message: str, session_id: str) -> dict:

    checks = {
      "role_enforcer": self.role_enforcer.check(message),
      "abuse_filter": self.abuse_filter.check(message),
      "rate_limiter": self.rate_limiter.is_allowed(session_id),
      "injection_detector": self.injection_detector.check(message)
    }

    allowed = all(result.get("allowed", False) for result in checks.values())
    return {"allowed": allowed, "checks": checks}
    

  def guard_results_handler(self, result: dict) -> str:
    """Returns user-fiendly explanation of denied prompts."""
    if result.get("allowed", True):
      return ""

    # Predefined friendly message based on reasons
    reason_map = {
      "scope_violation": "🚫 This question is not allowed based on the assistant's current role.",
      "abuse_detected": "⚠️ Please avoid abusive or offensive language.",
      "prompt_injection": "⚠️ Suspicious input detected. Please rephrase your query.",
      "rate_limited": "⏳ You're sending messages too quickly. Please wait a moment.",
      "unknown": "⚠️ Your input was blocked due to an unspecified policy."
    }

    messages = []
    for name, res in result.get("checks", {}).items():
      if not res.get("allowed", True):
        reason = res.get("reason", "unknown")
        details = res.get("details", "")
        friendly_message = reason_map(reason, reason_map["unknown"])
        messages.append(f"❌ {name}: {friendly_message}" + (f"\n→ {details}" if details else ""))

    return "\n\n".join(messages)