from typing import List, Dict
import fitz


def extract_pdf_text(path: str) -> List[Dict[str, str]]:
  """Extracts text per page and returns List of Dictionary with metadata."""
  doc = fitz.open(path)
  pages = []
  for i, page in enumerate(doc):
    text = page.get_text()
    if text.strip():
      pages.append({
        "text": text.strip(),
        "metadata": {
          "source": path.split("/")[-1],
          "page": i + 1
        }
      })
  return pages

