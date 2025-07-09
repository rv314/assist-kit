import os
from core.utils.evaluation_logger import parse_qa

DEBUG = os.getenv("DEBUG", "false").lower() == "true"

def debug_log(log_msg: str, prefix: str = "DEBUG: "):
  """Print debug messages only if debug is enabled"""
  if DEBUG:
    print(f"{prefix}: {log_msg}")


""" def print_vector_results(results: list[tuple[str, float]]):
  "Pretty print retrieved context with scores."
  if not results:
    print("No content found in vector DB.")
    return
  
  print("Retrieved context messages:")
  for idx, (doc, score) in enumerate(results, 1):
    print(f"  [{idx}] Score: {score:.4f} | Content: {doc[:80]}...") """

def print_vector_results(results: list):
  """Pretty print retrieved context with optional scores."""
  if not results:
    print("No content found in vector DB.")
    return

  print("Retrieved context messages:")
  for idx, (doc, score) in enumerate(results, 1):
    qa = parse_qa(doc)
    print(f"\n  [{idx}] Score: {score:.4f}")
    if "question" in qa and "answer" in qa:
      print(f"    Q: {qa['question']}")
      print(f"    A: {qa['answer']}")
    else:
      print(f"    {qa.get('raw', '')[:100]}...")
    # if isinstance(item, tuple) and len(item) == 2:
    #   doc, score = item
    #   print(f"  [{idx}] Score: {score:.4f} | Content: {doc[:80]}...")
    # else:
    #   print(f"  [{idx}] Content: {str(item)[:80]}...")


def print_eval_log(query: str, response: str, context_results: list[tuple[str, float]]):
  """Print evaluation result in readable format"""
  print(f"\n Evaluation log")
  print(f" Query: {query}")
  print_vector_results(context_results)
  print(f" Response: {response}")

def str_to_bool(value: str) -> bool:
  return value.strip().lower() in ["1", "true", "yes"]