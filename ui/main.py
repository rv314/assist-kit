from nicegui import ui, app
from ui.pages import home, chat, rag
from ui.pages.chat import render

dark_mode_state = None

# Route definitions
@ui.page("/")
def route_home():
    home.render()

    def update_dark_mode_state():
        global dark_mode_state
        dark_mode_state = dark.value
    dark = ui.dark_mode().bind_value(app.storage.user, 'dark_mode')
    ui.switch('Dark mode').bind_value(dark)

    dark.on_value_change(update_dark_mode_state)

@ui.page("/chat")
def route_chat():
    chat.render()

@ui.page("/rag")
def route_rag():
    rag.render()

def create_app(reload=False):
    app.native.window_args["title"] = "AssistKit"
    ui.run(reload=reload, storage_secret="secret!")

# Start the app
if __name__ in {"__main__", "__mp_main__"}:
    create_app()