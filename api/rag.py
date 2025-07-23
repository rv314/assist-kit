from fastapi import FastAPI, APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from typing import Optional
from uuid import UUID, uuid4
from bleach import clean

from core.engine.rag_engine import RAGEngine
from core.utils.config import load_config

router = APIRouter()
app = FastAPI()
app.include_router(router)

# Load config
config = load_config()
rag_engine = RAGEngine(config=config)

# ------------ Request / Response Models -----------------
class RagQueryRequest(BaseModel):
  query: str
  session_id: Optional[UUID] = None
  top_k: Optional[int] = 3

class RagQueryResponse(BaseModel):
  response: str
  source_count: int

class RagIngestResponse(BaseModel):
  message: str
  chuncks_stored: int

# ------------- Endpoints -------------------------------
@router.post("/rag/ingest", response_model=RagIngestResponse)
async def ingest(file: UploadFile = File(...)):
  if not file.filename.endswith(".pdf"):
    raise HTTPException(status_code=400, detail="Only PDF files are supported")
  
  # Save uploaded file temporarily
  temp_path = f"/tmp/{file.filename}"
  with open(temp_path, "wb") as f:
    content = await file.read()
    f.write(content)

  try:
    chunks = rag_engine.ingest_pdf(temp_path)
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Ingestion Failed: {str(e)}")
  
  return RagIngestResponse(message="PDF ingested successfully", chuncks_stored=len(chunks))


@router.post("/rag/query", response_model=RagQueryResponse)
async def query_rag(request: RagQueryRequest):
  try:
    answer = rag_engine.query(request.query, top_k=request.top_k)
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Query Failed: {str(e)}")
  
  return RagQueryResponse(response=answer, source_count=request.top_k)