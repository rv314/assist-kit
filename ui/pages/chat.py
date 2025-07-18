from nicegui import ui, run
from core.utils.config import load_config
from datetime import datetime
import uuid
import requests

# TODO:
# 1. Dialog instead of drop-down for model selection
# 2. Dark mode / Theme global setting
# 3. Welcome message by assistant and current setup/prompt

class Chat():
  def __init__(self):
    self.config = load_config()
    self.messages = []
    self.chat_area = None
    self.input_box = None
    self.model_selector = None
    self.AVATARS = self.config.get("avatars")
    self.session_id = str(uuid.uuid4()) # temporary session id until login feature is implemented
    self.selected_model = self.config["llm"]["model"]

    self.render()

  def render(self):
    dark = ui.dark_mode().enable()
    ui.markdown("## 💬 AssistKit — AI Assistant").classes("text-center")

    # Placeholder for injecting chat UI after model selection
    self.chat_container = ui.element("div").classes("w-full max-w-4xl m-auto mt-10")

    def select_model():
      with ui.dialog() as dialog:
        with ui.card():
          ui.markdown("### 🔧 Select a model")
          model_selector = ui.select(
            self.config["llm"]["available_models"],
            label="Choose a model",
            value=self.config["llm"]["model"]
            )
          ui.button("Start", on_click=lambda: (dialog.close(), start_chat(model_selector.value)))
          
          dialog.open()

    select_model()

    def start_chat(selected_model):
      self.selected_model = selected_model

      def scroll_to_bottom():
        ui.run_javascript("document.getElementById('chat-area').scrollTop = document.getElementById('chat-area').scrollHeight")
      
      # TODO: Load previous session messages if available (Where did below go?)
      # session_data = self.session_manager.load_session(self.session_id) or []
      # self.messages = session_data.get("messages", []) if session_data else []
  
      async def send_message():
        user_text = self.input_box.value.strip()
        if not user_text:
          return

        timestamp = datetime.now().strftime("%H:%M")
        # Show user message
        with self.chat_area:    
          with ui.row().classes("justify-end w-full"):
            user_avatar = self.AVATARS["user"]
            ui.chat_message(user_text, name="You", sent=True, avatar=user_avatar).props('bg-color=blue-2 color=primary')
            ui.label(timestamp).classes("text-xs text-gray-400 ml-2 mt-1")
        
        self.messages.append({"role": "user", "content": user_text})
        self.input_box.value = ""

        # Show assistant placeholder
        with self.chat_area:
          with ui.row().classes("justify-start") as assistant_container:
            spinner = ui.spinner('dots', size='lg', color='grey')

        # Send message to FastAPI backend
        async def get_response():
          try:
            response = await run.io_bound(lambda: requests.post(
                "http://localhost:8000/api/chat",
                json={
                  "session_id": self.session_id,
                  "message": user_text,
                  "messages": self.messages,
                  "model": self.selected_model
                },
                timeout=15,
              ))
            data = response.json()
            # print(data)
            assistant_container.clear()
            assistant_avatar = self.AVATARS["assistant"]
            if "guardrails_result" in data and not data["guardrails_result"].get("allowed", True):
              friendly_message = data["guardrails_result"].get("message", "⚠️ Blocked by guardrails.")
              with assistant_container:
                ui.chat_message(friendly_message, name="Guardrails", avatar=assistant_avatar).props("bg-color=red-1 text-red")
                ui.label(timestamp).classes("text-xs text-gray-400 ml-2 mt-1")
            else:
              assistant_message = data.get("response", "")
              with assistant_container:
                ui.chat_message(assistant_message, name="Assistant", avatar=assistant_avatar).props("bg-color=grey")
                ui.label(timestamp).classes("text-xs text-gray-400 ml-2 mt-1")
              self.messages.append({"role": "assistant", "content": assistant_message})
          
          except Exception as e:
            assistant_container.clear()
            ui.markdown(f"**❌ Error:** {str(e)}").classes("text-red-500")
      
          # Scroll to bottom
          scroll_to_bottom()
          
        ui.timer(0.1, get_response, once=True)
        scroll_to_bottom()

      # Build Chat UI
      with self.chat_container:
        with ui.card().classes("w-full max-w-4xl m-auto mt-10"): # verify div here
          with ui.element('div').classes("w-full h-[30rem] overflow-y-auto").props('id=chat-area') as self.chat_area:
            
            # Assistant welcome message
            with ui.row().classes("justify-start w-full"):
              assistant_avatar = self.AVATARS["assistant"]
              welcome_msg = self.config.get("llm")["welcome_message"]
              ui.chat_message(welcome_msg, name="Assistant", avatar=assistant_avatar).props("bg-color=grey")
              ui.label(datetime.now().strftime("%H:%M")).classes("text-xs text-gray-400 ml-2 mt-1")

          with ui.row().classes("w-full items-center mt-4"):
            self.input_box = ui.input(placeholder="Type your message...").props("rounded outlined").classes("w-full")
            self.input_box.on("keydown.enter", lambda e: send_message())
            ui.button("Send", on_click=send_message)
            ui.button("Clear", on_click=self.reset_chat).props("flat").classes("ml-2")  

  def reset_chat(self):
    self.messages.clear()
    self.chat_area.clear()