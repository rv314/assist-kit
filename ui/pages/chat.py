from nicegui import ui
from core.engine.chat_client import ChatEngine
from core.utils.config import load_config
from datetime import datetime
from core.engine.session_manager import SessionManager
from core.guardrails.guard_manager import GuardManager
import uuid

# TODO:
# 1. Dialog instead of drop-down for model selection
# 2. Dark mode / Theme global setting
# 3. Welcome message by assistant and current setup/prompt

class AssistKit():
  def __init__(self):
    self.config = load_config()
    self.chat_engine = None
    self.messages = []
    self.chat_area = None
    self.input_box = None
    self.model_selector = None
    self.AVATARS = self.config.get("avatars")
    self.session_manager = SessionManager(config=self.config.get("session_store", {}))
    self.guard_manager = GuardManager(self.config)
    self.session_id = str(uuid.uuid4()) # temporary session id until login feature is implemented

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
      self.config["llm"]["model"] = selected_model
      self.chat_engine = ChatEngine(config=self.config)
      
      # Load previous session messages if available
      session_data = self.session_manager.load_session(self.session_id) or []
      self.messages = session_data.get("messages", []) if session_data else []
  
      def send_message():
        user_text = self.input_box.value.strip()
        if not user_text:
          return
        
        # Guardrails check
        guard_result = self.guard_manager.check_all(user_text, session_id=self.session_id)
        if not guard_result["allowed"]:
          
          with self.chat_area:
            with ui.row().classes("justify-start w-full"):
              ui.chat_message(f"Blocked: {guard_result['reason']}\n{guard_result['details', '']}", name="GuardRails").props("bg-color=red-1 text-red")
              ui.label(timestamp).classes("text-xs text-gray-400 ml-2 mt-1")
      
        timestamp = datetime.now().strftime("%H:%M")
        # Show user message
        with self.chat_area:    
          with ui.row().classes("justify-end w-full"):
            user_avatar = self.AVATARS["user"]
            user_msg = ui.chat_message(user_text, name="You", sent=True, avatar=user_avatar).props('bg-color=blue-2 color=primary')
            ui.label(timestamp).classes("text-xs text-gray-400 ml-2 mt-1")
        

        self.messages.append({"role": "user", "content": user_text})
        self.input_box.value = ""

        # Show spinner
        with self.chat_area:
          with ui.row().classes("justify-start") as assistant_container:
            spinner = ui.spinner('dots', size='lg', color='grey')

        def scroll_to_bottom():
          ui.run_javascript("document.getElementById('chat-area').scrollTop = document.getElementById('chat-area').scrollHeight")


        def get_response():
          response = self.chat_engine.chat(self.messages)
          self.messages.append({"role": "assistant", "content": response})
          self.session_manager.save_session(self.session_id, self.messages)

          assistant_container.clear()
          with assistant_container:
            assistant_avatar = self.AVATARS["assistant"]
            ui.chat_message(response, name="Assistant", avatar=assistant_avatar).props("bg-color=grey")
            ui.label(timestamp).classes("text-xs text-gray-400 ml-2 mt-1")

            # Scroll to bottom
            scroll_to_bottom()
          
        ui.timer(0.1, get_response, once=True)
        scroll_to_bottom()

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

  

  
""" 
def render():
    global chat_engine
    dark = ui.dark_mode().enable()

    def select_model():
       with ui.dialog() as dialog:
          with ui.card():
             ui.markdown("### 🔧 Select a model")
             model_selector = ui.select(
                config["llm"]["available_models"],
                label="Choose a model",
                value=config["llm"]["model"]
             )
             ui.button("Start", on_click=lambda: (dialog.close(), start_chat(model_selector.value)))
          dialog.open()

    def start_chat(selected_model):
      config["llm"]["model"] = selected_model
      global chat_engine
      chat_engine = ChatEngine(config=config)

      # UI card layout
      with ui.card().classes("w-full max-w-4xl m-auto mt-10"):
        ui.markdown("## 💬 AssistKit — AI Assistant")

      with ui.element('div').classes("w-full h-[30rem] overflow-y-auto").props('id=chat-area') as chat_area:
        pass  # messages will be added here

      with ui.row().classes("w-full items-center mt-4"):
        input_box = ui.input(placeholder="Type your message...").props("rounded outlined").classes("w-full")
        send_button = ui.button("Send", color="primary")


      def send_message(self):
        user_text = input_box.value.strip()
        if not user_text:
          return

        timestamp = datetime.now().strftime("%H:%M")
        
        # 1. Show user message instantly
        with chat_area:
          with ui.row().classes("justify-end w-full"):
            user_avatar = AVATARS["user"]
            user_msg = ui.chat_message(user_text, name="You", sent=True, avatar=user_avatar).props('bg-color=blue-2 color=primary')
            ui.label(timestamp).classes("text-xs text-gray-400 ml-2 mt-1")
          

        messages.append({"role": "user", "content": user_text})
        input_box.value = ""

        # 3. Show assistant placeholder in container
        with chat_area:
          with ui.row().classes("justify-start w-full") as assistant_container:
            spinner = ui.spinner('dots', size='lg', color='grey')

        # 4. Call backend and get response
        def get_response():
          response = chat_engine.chat(messages)
          messages.append({"role": "assistant", "content": response})
          
        # 5. Remove placeholder and show response
          with chat_area:
            assistant_container.clear()
            with assistant_container:
              assistant_avatar = AVATARS["assistant"]
              ui.chat_message(response, name="Assistant", avatar=assistant_avatar).props('bg-color=grey color=green')
              ui.label(datetime.now().strftime("%H:%M")).classes("text-xs text-gray-400 ml-2 mt-1")

          scroll_to_bottom()

        # Non-blocking
        ui.timer(0.1, get_response, once=True)
        scroll_to_bottom()

        # Wire butting and Enter key
        send_button.on("click", send_message)
        input_box.on("keydown.enter", lambda e: send_message())

    select_model() """