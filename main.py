from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from nicegui import app as nicegui_app, ui
from ui.pages import chat
from api.chat import router as chat_router


chat.AssistKit()

# FastAPI backend
app = FastAPI()

# Enable CORS
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api")