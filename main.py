from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.chat import router as chat_router
from api.rag import router as rag_router
import logging


logging.basicConfig(level=logging.DEBUG)

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

# Mount backend API routers to NiceGUI FastAPI app
app.include_router(chat_router, prefix="/api")
app.include_router(rag_router, prefix="/api")