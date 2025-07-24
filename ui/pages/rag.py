from nicegui import ui
import httpx

API_BASE = "http://localhost:8000/api/rag"

def render():
    ui.label("📄 Document Q&A (RAG)").classes("text-xl font-bold")
    ui.markdown("Upload a PDF and ask questions based on its content.")
    
    status = ui.label().classes("text-green-600")
    error = ui.label().classes("text-red-500")

    uploaded_file_name = None

    def handle_upload(e):
        nonlocal uploaded_file_name
        uploaded_file_name = e.name

        try:
            files = {'file': (e.name, e.content.read(), 'application/pdf')}
            response = httpx.post(f'{API_BASE}/ingest', files=files)

            if response.status_code == 200:
                data = response.json()
                status.set_text(f"{data['message']} ({data['chunks_stored']} chunks stored)")
                error.set_text("")
            else:
                error.set_text(f"Error: {response.json().get('detail', 'Unknown Error')}")
        except Exception as e:
            error.set_text(f"Exception during upload: {e}")

    ui.upload(
        label="Upload PDF",
        auto_upload=True,
        max_files=1,
        on_upload=handle_upload,
    ).props('accept=.pdf')

    with ui.column().classes("mt-6"):
        ui.label("Ask a question about the document:").classes("text-md font-semibold")
        query_input = ui.input(placeholder="Type your question...").classes("w-full")

        answer_label = ui.label().classes("text-blue-700 font-medium mt-2")

        def ask_question():
            question = query_input.value.strip()
            if not question:
                error.set_text("Please enter a question")
                return
            
            try:
                response = httpx.post(f"{API_BASE}/query",
                                      json={
                                          "query": question,
                                          "top_k": 3
                                            })
                if response.status_code == 200:
                     data = response.json()
                     answer_label.set_text = f"Answer: {data['response']}"
                     error.set_text("")
                else:
                    error.set_text(f"Query error: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                error.set_text(f"Exception during query: {e}")

        ui.button("Ask", on_click=ask_question).props("color=secondary")