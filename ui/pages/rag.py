from nicegui import ui


def render():
    ui.label("📄 Document Q&A (RAG)").classes("text-xl font-bold")
    ui.markdown("Upload a PDF and ask questions based on its content.")
    # TODO: Upload + parse + context query