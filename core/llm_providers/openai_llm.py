import openai
import os
from dotenv import load_dotenv
from registries.llm_registry import register_llm

load_dotenv()


@register_llm("openai")
class OpenAIChatModel:
  def __init__(self, config: dict):
    self.model = config.get("model", "gpt-3.5-turbo")
    openai.api_key = os.getenv("OPENAI_API_KEY")

  
  def chat(self, messages):
    resp = openai.chat.completions.create(
      model = self.model,
      messages = messages
    )
    return resp.choices[0].message.content
  