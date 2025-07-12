import time
from collections import defaultdict, deque

class RateLimiter:
  def __init__(self, config=None):
    self.config = config or {}
    self.max_requests = self.config.get("max_requests", 5)
    self.time_window = self.config.get("time_window", 60) # 5 requests per minute 

    # {session_id: deque[timestamps]}
    self.request_log = defaultdict(deque)


  def is_allowed(self, session_id: str) -> dict:
    """Returns whether the session is within allowed rate limit."""
    now = time.time()
    timestamps = self.request_log[session_id]

    # Remove timestamps outside the allowed window
    while timestamps and (now - timestamps[0]) > self.time_window:
      timestamps.popleft()

    if len(timestamps) >= self.max_requests:
      retry_after = self.time_window - (now - timestamps[0])
      return {
        "allowed": False,
        "reason": "rate_limited",
        "details": f"{len(timestamps)} messages sent in last {self.time_window} seconds, limit is {self.max_requests}."
      }
    
    timestamps.append(now)
    return {"allowed": True}