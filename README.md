# AssistKit 🧠

**Modular GenAI Assistant Framework**  
An extensible, pluggable framework to build powerful, context-aware assistants for multiple domains and tasks — including Chat, RAG (Retrieval-Augmented Generation), and more.

---

## 🚀 Overview

**AssistKit** is designed as a modular backend assistant engine that powers intelligent interactions using LLMs and embeddings.  
Built with extensibility in mind, it supports multiple use cases:

- 💬 **Chat Assistant** with memory (chat_logs)
- 📄 **RAG Pipeline** for PDF, website, or custom document Q&A
- 🧩 Plugin-style architecture for future tools like Web Search, SQL Agent, etc.
- 🔗 Pluggable registries for LLMs, Embedders, and Vector DBs
- 🖥️ **NiceGUI Frontend**: Clean UI layer for interacting with AssistKit via web browser (Planning to switch to Next.js or other framework in future)

---

## 🔧 Current Modules

| Module          | Description                                              |
|-----------------|----------------------------------------------------------|
| `api/chat.py`   | Handles user chat, stores context in `chat_logs` vector  |
| `orchestrator.py` | Coordinates model interaction and context retrieval |
| `session_manager.py` | Handles chat sessions (JSON for now, pluggable)     |
| `vector_store.py` | Stores and retrieves documents from Vector DB          |
| `prompt_loader.py` | Loads system prompts dynamically from templates       |

---

## 🧠 Architecture
```bash
User → FastAPI (api/chat or api/rag)
→ Orchestrator (InteractionEngine)
├─ get_llm() from llm_registry
├─ get_embedder() from embedding_registry
├─ get_vector_db() from vector_registry
└─ vector_store → stores/queries via embeddings
```
- **ChatEngine**: Current base class in orchestrator; will be subclassed by `RAGEngine`, `WebSearchEngine`, etc.
- **Embeddings & LLMs**: Abstracted behind registries for easy swapping
- **Collections**: Support for multiple vector DB collections (e.g., `chat_logs`, `rag_docs`)

---

## 📁 Folder Structure (WIP)
```bash
|-- api
|   `-- chat.py
|-- core
|   |-- __init__.py
|   |-- agents
|   |-- config
|   |-- embedding_models
|   |-- engine
|   |-- guardrails
|   |-- llm_providers
|   |-- prompts
|   |-- rag
|   |-- registries
|   |-- session_backends
|   |-- utils
|   |-- vector_backends
|-- documents
|   |-- examples
|   |-- processed
|   |-- uploads
|-- main.py
|-- session_data
|   |-- session_data.json
|-- tests
|   |-- __init__.py
|   |-- test_chat_client.py
|   |-- test_token_utils.py
|   |-- test_vectorstore.py
|-- ui
|   |-- __init__.py
|   |-- components
|   |-- main.py
|   |-- pages
|-- vectors
    |-- chroma
```

---

## 🔜 Roadmap

- ✅ RAG Engine using uploaded files or web-scraped content
- 🗂 Pluggable storage backends (JSON → Redis/PostgreSQL)
- 🧾 PDF and Web QA pipelines
- 🔍 Web Search Agent / Other Agents / Agent Design Patterns
- Model Context Protocol (MCP)
- ☁️ Deployable Dockerfile and Installation Guide

## Research (Planning to include) 

- Knowledge Graph (Neo4j or other Open Source)

## Use Cases

Idea to build this framework is to re-utilize it for various purposes / use-cases. Currently focusing on building the foundations.

---

## 📌 Notes

- The current focus is on **local development**, so installation and deployment instructions will be added soon.
- LLM and Embedding provider is **OpenAI** and vector DB is **Chroma** (pluggable).
- Sessions are currently stored in JSON files but are designed to switch backends easily.

---

## 🧑‍💻 Contributing

Feature suggestions, refactors, or bug reports are welcome.  
To contribute:

1. Fork the repo
2. Create a feature branch
3. Submit a pull request with your changes and description

---

## 📄 License

MIT License

---
