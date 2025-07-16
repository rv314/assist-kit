import json
import os
from datetime import datetime
import re


EVAL_LOG_FILE = "logs/eval_log.jsonl"

# Confirm directory exists
os.makedirs("logs", exist_ok=True)


def parse_qa(entry: str) -> dict:
  """Parse stored vector entry into separate question and answer parts."""
  match = re.match(r"Q:\s*(.*?)\sA:\s*(.*)", entry, re.DOTALL)
  
  if match:
    return {"question": match.group(1).strip(), "answer": match.group(2).strip()}
  else:
    return {"raw": entry} # fallback if format doesnt match


def log_eval(query, context_results, response):
  log_entry = {
    "timestamp": datetime.now().isoformat(),
    "query": query,
    "top_k_context": [
      {**parse_qa(entry["text"]), "score": entry["score"]}
      for entry in context_results
    ],
    "response": response,
    "context_used": bool(context_results)
  }

  with open(EVAL_LOG_FILE, "a", encoding="utf-8") as f:
    f.write(json.dumps(log_entry) + "\n")