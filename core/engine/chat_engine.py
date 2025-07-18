# chat_engine.py
from core.engine.orchestrator import InteractionEngine
from typing import List, Dict
from core.utils.prompt_loader import load_prompt_template
from core.utils.token_limits import trim_messages
from core.utils.debug import debug_log, print_eval_log, print_vector_results
from core.utils.evaluation_logger import log_eval


class ChatEngine(InteractionEngine):
  def __init__(self, config):
    super().__init__(config, collection_name="chat_logs")


  def get_context(self, query: str, k: int = 3):
      """Retrieve top-k similar Q&A from vector store to dynamically use as context in system prompt."""
      context_results = self.vector_store.similarity_search(query, k)
      context_text = "\n---\n".join([doc["text"] for doc in context_results]) if context_results else ""
      return context_text, context_results
  
  def run(self, messages: List[Dict[str, str]]) -> str:

    """Dynamically builds prompt using context, calls model API -> sends prompt and returns response"""
    user_input = messages[-1]["content"]

    # Step 1. Fetch relevant context
    context_text, context_results = self.get_context(user_input)

    # Step 2. Build system prompt with context if available
    template = load_prompt_template()
    prompt_content = template.replace("{{context}}", context_text if context_text else "")
    system_prompt = {"role": "system", "content": prompt_content}
    
    # Step 3. Trim and finalize message history
    full_prompt = [system_prompt] + messages[-2:] # Only last 2 user/assistant messages
    full_prompt = trim_messages(full_prompt, model=self.model, max_tokens=self.max_tokens)

    # Step 4. Debug if enabled
    if self.debug:
      import json
      print("\n📌 Prompt sent to OpenAI:")
      dumped_json = json.dumps(full_prompt, indent=2)
      print(dumped_json[:1500] + "..." if len(json.dumps(full_prompt)) > 1500 else dumped_json)
      print("\n📌 Context used:", "Yes" if context_text else "No")
      print_vector_results(context_results)
      debug_log(f"User input: {user_input}")
      debug_log(f"Context count: {len(context_results)}")
      for idx, (doc, score) in enumerate(context_results, 1):
        debug_log(f"[{idx}] (score: {score:.4f}) {doc}")

    # Step 5. Get response from model
    try:
      reply = self.llm.chat(full_prompt)
    except Exception as e:
      reply = "An error occured while generating response, Check logs."
      debug_log(f"Model API error: {e}")

    # Step 6. Log results
    log_eval(user_input, context_results, reply)
    if self.debug:
      print(f"In chat_client Debug is set to: {self.debug}")
      print_eval_log(user_input, context_results, reply)

    # Step 7. Add messages to vector DB
    self.vector_store.log_chat_qa(user_input, reply)

    return reply
