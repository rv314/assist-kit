from nicegui import ui
from core.engine.chat_client import ChatEngine
from core.utils.config import load_config
from datetime import datetime


def render():
    dark = ui.dark_mode().enable()
    config = load_config()
    chat_engine = ChatEngine(config=config)
    messages = []

    # UI card layout
    with ui.card().classes("w-full max-w-4xl m-auto mt-10"):
        ui.markdown("## 💬 AssistKit — AI Assistant")

        with ui.element('div').classes("w-full h-[30rem] overflow-y-auto").props('id=chat-area') as chat_area:
            pass  # messages will be added here

        with ui.row().classes("w-full items-center mt-4"):
            input_box = ui.input(placeholder="Type your message...").props("rounded outlined").classes("w-full")
            send_button = ui.button("Send", color="primary")

    def scroll_to_bottom():
      ui.run_javascript("document.getElementById('chat-area').scrollTop = document.getElementById('chat-area').scrollHeight")


    def send_message():
      user_text = input_box.value.strip()
      if not user_text:
        return

      timestamp = datetime.now().strftime("%H:%M")
        
      # 1. Show user message instantly
      with chat_area:
         with ui.row().classes("justify-end w-full"):
          user_avatar = 'https://cdn-icons-png.flaticon.com/512/1077/1077012.png'
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
            assistant_avatar = 'https://cdn-icons-png.flaticon.com/512/4712/4712027.png'
            ui.chat_message(response, name="Assistant", avatar=assistant_avatar).props('bg-color=grey color=green')
            ui.label(datetime.now().strftime("%H:%M")).classes("text-xs text-gray-400 ml-2 mt-1")

        scroll_to_bottom()

      # Non-blocking
      ui.timer(0.1, get_response, once=True)
      scroll_to_bottom()

    # Wire butting and Enter key
    send_button.on("click", send_message)
    input_box.on("keydown.enter", lambda e: send_message())