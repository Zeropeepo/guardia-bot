# Guardia Bot 🛡️

Guardia Bot is a comprehensive cybersecurity tutor powered by Retrieval-Augmented Generation (RAG). It helps beginners and professionals alike learn about cybersecurity concepts by leveraging a curated knowledge base of cybersecurity documents. 

## 🌟 Features

- **Educational RAG Pipeline:** Retrieves accurate and relevant information using advanced semantic search and reranking.
- **Detailed Citations:** Provides transparency by citing the original sources (documents and relevance scores) for every generated answer.
- **Built-in Guardrails:** Protects against prompt injection attacks and ensures the bot remains focused on its educational purpose.
- **FastAPI Backend:** A robust, asynchronous API handling ingestion, retrieval, and evaluation.
- **Streamlit Frontend:** An interactive, user-friendly chat interface with topic and level filtering.
- **Systematic Evaluation:** Includes an automated evaluation pipeline using `ragas` to measure faithfulness, relevancy, and context recall.

## 🏗️ Architecture Stack

- **Backend:** [FastAPI](https://fastapi.tiangolo.com/)
- **Frontend:** [Streamlit](https://streamlit.io/)
- **Vector Database:** [Qdrant](https://qdrant.tech/) (Dockerized)
- **RAG Framework:** [LlamaIndex](https://www.llamaindex.ai/)
- **Embeddings:** Jina AI (`jina-embeddings-v3`)
- **LLM:** Groq (`llama-3.3-70b-versatile`)
- **Package Manager:** [uv](https://github.com/astral-sh/uv)

---

## 🚀 Getting Started

### 1. Prerequisites

Make sure you have the following installed on your machine:
- **Python 3.11+**
- **Docker** and **Docker Compose**
- **uv** (fast Python package manager — recommended, but optional)
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

### 2. Configure API Keys

Copy the example environment file and fill in your API keys:

```bash
cp .env.example .env
```

Open `.env` and set:
- `JINA_API_KEY`: Get this from [Jina AI](https://jina.ai/) — used for embeddings and reranking.
- `GROQ_API_KEY`: Get this from [Groq](https://console.groq.com/) — used for LLM inference.

> All other values in `.env` are pre-configured and ready to use.

### 3. Run the App

```bash
chmod +x run.sh
./run.sh
```

The script handles everything automatically:
- ✅ Starts Qdrant vector database (Docker)
- ✅ Creates virtual environment and installs dependencies (if not present)
- ✅ Ingests the default cybersecurity knowledge base (skipped if already done)
- ✅ Starts FastAPI backend at [http://localhost:8000](http://localhost:8000)
- ✅ Opens Streamlit chat UI at [http://localhost:8501](http://localhost:8501)

Press `Ctrl+C` to stop all services gracefully.

---

### Manual Startup (Alternative)

If you prefer to set up manually:

```bash
# 1. Create and activate virtual environment
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt

# 2. Start Qdrant
docker compose up -d

# 3. Ingest documents
python scripts/ingest_defaults.py

# 4. Start backend (Terminal 1)
uvicorn app.main:app --reload

# 5. Start frontend (Terminal 2)
streamlit run frontend/streamlit_app.py
```



---

## 📚 Managing the Knowledge Base

Before Guardia Bot can answer questions, you need to ingest some documents into the vector store. 

You can upload documents (like PDFs, TXT, or Markdown) directly through the FastAPI swagger dashboard:
1. Go to [http://localhost:8000/docs#/ingest/ingest_document_api_ingest_post](http://localhost:8000/docs#/ingest/ingest_document_api_ingest_post)
2. Upload a cybersecurity document and assign an optional `topic` and `level` (e.g., beginner, intermediate).
3. The pipeline will automatically parse, chunk, embed, and store the document in Qdrant.

## 📊 RAG Evaluation

Guardia Bot includes a built-in evaluation framework using the `ragas` library.

To test the quality of your RAG pipeline:
1. Ensure your knowledge base has been populated with relevant documents.
2. Send a POST request to `/api/eval` with an array of questions and their expected "ground truth" answers.
3. The system will evaluate the retrieval precision, context recall, answer relevancy, and faithfulness, returning detailed metrics for continuous improvement.
