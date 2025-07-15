from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from core.engine.chat_client import ChatEngine
from core.utils.config import load_config
from core.engine.session_manager import SessionManager
from core.guardrails.guard_manager import GuardManager
from typing import Optional
from uuid import uuid4

router = APIRouter()
config = load_config()
chat_engine = ChatEngine(config=config)
session_manager = SessionManager(config=config.get("session_store", {}))
guard_manager = GuardManager(config)

# --------- Request and Response Schema ----------
class ChatRequest(BaseModel):
  session_id: Optional[str] = None
  message: str

class ChatResponse(BaseModel):
  response: str
  allowed: bool = True
  reason: str = ""
  details: str = ""

# ------- Endpoint --------
@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
  # print(f">>> Received message: {request.message}")
  session_id = request.session_id or str(uuid4())
  message = request.message

  # GuardRails
  guard_result = guard_manager.get_all_guard_results(message, session_id)

  if not guard_result.get("allowed"):
    reason = guard_manager.guard_results_handler(guard_result)
    return ChatResponse(
      response=reason,
      allowed=False,
      reason="guardrails_triggered",
      details=reason
    )
  
  # Load session
  messages = session_manager.load_session(session_id)
  if not messages:
    messages = []
  messages.append({"role": "user", "content": message})

  # Call chat engine
  reply = chat_engine.chat(messages)
  # print(f" Assistant response: {reply}")
  messages.append({"role": "assistant", "content" : reply})

  # Save session
  session_manager.save_session(session_id, messages)

  return ChatResponse(response=reply)