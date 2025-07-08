from utils.token_limits import count_tokens, trim_messages
import pytest
import os

openai_key = os.getenv("OPENAI_API_KEY")


@pytest.mark.skipif(not openai_key, reason="OpenAI key not found!!")
def test_count_tokens():
    messages = [
        {"role": "user", "content": "hello " * 3500}  # ~3000+ tokens
    ]
    model = "gpt-3.5-turbo"
    total = count_tokens(messages, model)
    assert total > 3000, f"Expected > 3000 tokens, got {total}"
    print("✅ test_count_tokens passed.")

def test_trim_messages():
    messages = [
        {"role": "user", "content": "hello " * 3500},  # Large message
        {"role": "user", "content": "short message"}
    ]
    model = "gpt-3.5-turbo"
    trimmed = trim_messages(messages, model, max_tokens=3000)
    # The large message will be dropped, but short one will remain
    assert any("short message" in msg["content"] for msg in trimmed), "Expected short message to remain"
    print("✅ test_trim_messages passed.")

if __name__ == "__main__":
    test_count_tokens()
    test_trim_messages()