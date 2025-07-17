# tests/test_chat_client.py

from core.engine.orchestrator import chat
import pytest
import os

openai_key = os.getenv("OPENAI_API_KEY")


@pytest.mark.skipif(not openai_key, reason="OpenAI key not found!!")
def test_chat():
  messages = [
    {"role": "system", "content": "You are helpful assistant."},
    {"role": "user", "content": "What is your purpose?"}
  ]

  reply = chat(messages)
  assert isinstance(reply, str) and len(reply) > 0
  print("✅ test_chat_with_gpt passed.")


if __name__ == '__main__':
  test_chat()