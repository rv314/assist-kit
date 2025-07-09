from nicegui import ui, app

def render():
  ui.label("👋 Welcome to AssistKit").classes("text-2xl font-bold")
  ui.markdown("Navigate to [Chat](/chat) or [RAG](/rag)")