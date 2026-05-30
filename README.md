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
- **LLM:** Groq (`mixtral-8x7b-32768`)
- **Package Manager:** [uv](https://github.com/astral-sh/uv)

---

## 🚀 Getting Started

### 1. Prerequisites

Make sure you have the following installed on your machine:
- **Python 3.11+**
- **Docker** and **Docker Compose**
- **uv** (Extremely fast Python package installer and resolver)
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

### 2. Setup the Environment

Initialize the virtual environment and install the required dependencies using `uv`:

```bash
# Create a virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory by copying the example provided:

```bash
cp .env.example .env
```

Open the `.env` file and fill in your API keys:
- `JINA_API_KEY`: Get this from [Jina AI](https://jina.ai/) for embeddings and reranking.
- `GROQ_API_KEY`: Get this from [Groq](https://groq.com/) for lightning-fast LLM inference.

### 4. Start the Vector Database (Qdrant)

The RAG pipeline requires a vector database to store document embeddings. We use a locally hosted Qdrant container.

```bash
docker compose up -d
```
*Note: You can view the Qdrant dashboard at [http://localhost:6333/dashboard](http://localhost:6333/dashboard)*

---

## 🏃‍♂️ Running the Application

To run the application, you need to start both the FastAPI backend and the Streamlit frontend. It is recommended to run them in **separate terminal windows**.

### Step 1: Start the Backend API

In your first terminal window, activate the environment and start the API:

```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`. 
Interactive API documentation (Swagger UI) is automatically generated at [http://localhost:8000/docs](http://localhost:8000/docs).

### Step 2: Start the Frontend UI

Open a **new terminal window**, activate the environment, and start Streamlit:

```bash
source .venv/bin/activate
streamlit run frontend/streamlit_app.py
```
The Streamlit interface will open in your browser at [http://localhost:8501](http://localhost:8501).

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
