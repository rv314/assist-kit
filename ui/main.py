from nicegui import ui, app
from ui.pages import chat, home, rag
from ui.pages.chat import Chat

dark_mode_state = None

def setup_dark_mode():
    global dark_mode_state
    dark = ui.dark_mode().bind_value(app.storage.user, 'dark_mode')
    ui.switch('Dark Mode').bind_value(dark)

    @dark.on_value_change
    def on_change():
        nonlocal dark
        dark_mode_state = dark.value
        
# Route definitions
@ui.page("/")
def route_home():
    home.render()
    setup_dark_mode()

"""     def update_dark_mode_state():
        global dark_mode_state
        dark_mode_state = dark.value
    dark = ui.dark_mode().bind_value(app.storage.user, 'dark_mode')
    ui.switch('Dark mode').bind_value(dark)

    dark.on_value_change(update_dark_mode_state) """

@ui.page("/chat")
def route_chat():
    Chat()

@ui.page("/rag")
def route_rag():
    rag.render()

def create_app(reload=False):
    app.native.window_args["title"] = "AssistKit"
    ui.run(reload=reload, storage_secret="secret!")

# Start the app
if __name__ in {"__main__", "__mp_main__"}:
    create_app()