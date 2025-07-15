from fastapi import FastAPI, APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, constr, Field, ValidationError

from typing import Optional, Annotated
from uuid import UUID, uuid4
from bleach import clean

from core.engine.chat_client import ChatEngine
from core.utils.config import load_config
from core.engine.session_manager import SessionManager
from core.guardrails.guard_manager import GuardManager


router = APIRouter()

app = FastAPI()
app.include_router(router)

config = load_config()
chat_engine = ChatEngine(config=config)
session_manager = SessionManager(config)
guard_manager = GuardManager(config)

# --------- Request and Response Schema ----------
class ChatRequest(BaseModel):
  session_id: UUID = Field(default_factory=uuid4)
  message: Annotated[str, constr(strip_whitespace=True, min_length=1, max_length=1000)]

class ChatResponse(BaseModel):
  response: Annotated[str, constr(strip_whitespace=True)]
  allowed: bool = True
  reason: Optional[str] = ""
  details: Optional[str] = ""

# --------- Error Handler ----------------
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
  return JSONResponse(
    status_code=422,
    content={
      "error": "Validation Failed",
      "details": exc.errors(),
    },
  )

# ------- Endpoint --------
@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
  # print(f">>> Received message: {request.message}")
  session_id = request.session_id or str(uuid4())
  ## HTML sanitization using "clean" to strip dangerous tags
  message = clean(request.message)

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