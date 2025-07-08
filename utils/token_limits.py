import tiktoken

# token budget limit

def count_tokens(messages, model: str):
  encoding = tiktoken.encoding_for_model(model)
  total = 0
  for msg in messages:
    content = msg.get("content", "")
    role = msg.get("role", "")
    total += len(encoding.encode(role + content))
  return total


def trim_messages(messages, model: str, max_tokens=3000):
  encoding = tiktoken.encoding_for_model(model)
  total_tokens = 0
  trimmed = []

  # Reverse iterate to keep latest messages
  for msg in reversed(messages):
    role = msg.get("role", "")
    content = msg.get("content", "")
    msg_tokens = len(encoding.encode(role + content))
    
    if total_tokens + msg_tokens <= max_tokens:
      trimmed.insert(0, msg)
      total_tokens += msg_tokens
    else:
      break

  return trimmed