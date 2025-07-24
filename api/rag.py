from fastapi import FastAPI, APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import tempfile

from typing import Optional, Dict, List
from uuid import UUID, uuid4
from bleach import clean

from core.engine.rag_engine import RAGEngine
from core.engine.vector_store import VectorStore
from core.utils.config import load_config
from core.registries.embedding_registry import get_embedder

router = APIRouter()

# Load config
config = load_config()
rag_engine = RAGEngine(config=config)
embedder = get_embedder(config["embedding"]["provider"])
vector_store = VectorStore(full_config=config, embedder=embedder)
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

class TestChunk(BaseModel):
  id: str
  text: str
  metadata: Dict[str, str]

# ------------- Endpoints -------------------------------
## Testing
@router.post("/rag/test-ingest")
async def test_ingest(chunks: List[TestChunk]):
  print(chunks)
  try:
      vector_store.add_documents([
          {"id": chunk.id, "text": chunk.text, "metadata": chunk.metadata}
          for chunk in chunks
      ])
  except Exception as e:
      raise HTTPException(status_code=500, detail=f"Test ingestion failed: {str(e)}")

  return {"message": "Test ingestion succeeded", "chunks": len(chunks)}

@router.post("/rag/ingest", response_model=RagIngestResponse)
async def ingest(file: UploadFile = File(...)):
  if not file.filename.endswith(".pdf"):
    raise HTTPException(status_code=400, detail="Only PDF files are supported")
  
  try:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
      temp.write(await file.read())
      temp_path = temp.name

  
    chunks = rag_engine.ingest_pdf(temp_path)
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Ingestion Failed: {str(e)}")
  
  return RagIngestResponse(message="PDF ingested successfully", chuncks_stored=len(chunks))


@router.post("/rag/query", response_model=RagQueryResponse)
async def query_rag(request: RagQueryRequest):
  try:
    query = clean(request.query, tags=[], attributes={}, strip=True)
    answer = rag_engine.query(query, top_k=request.top_k)
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Query Failed: {str(e)}")
  
  return RagQueryResponse(response=answer, source_count=request.top_k)