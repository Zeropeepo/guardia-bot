#!/bin/bash

set -e

echo "==========================================="
echo "🛡️  Starting Guardia Bot Environment..."
echo "==========================================="

# Auto-create .env from .env.example if it doesn't exist
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo -e "\n⚠️  No .env found. Copying from .env.example..."
        cp .env.example .env
        echo "⚠️  Please open .env and fill in your JINA_API_KEY and GROQ_API_KEY, then re-run this script."
        exit 1
    else
        echo "❌ Neither .env nor .env.example found. Cannot continue."
        exit 1
    fi
fi

echo -e "\n[1/4] Starting Vector Database (Qdrant)..."
docker compose up -d

echo -e "\n[2/4] Setting up Virtual Environment..."
if [ ! -f ".venv/bin/activate" ]; then
    echo "  Virtual environment not found. Creating and installing dependencies..."
    if command -v uv &> /dev/null; then
        uv venv
        uv pip install -r requirements.txt
    else
        echo "  'uv' not found, using standard python venv..."
        python3 -m venv .venv
        .venv/bin/pip install -r requirements.txt
    fi
    echo "  ✅ Dependencies installed."
fi
source .venv/bin/activate

echo -e "\n[3/4] Checking/Ingesting Default Knowledge Base..."
sleep 2
python scripts/ingest_defaults.py

echo -e "\n[4/4] Starting FastAPI Backend and Streamlit Frontend..."

# Function to handle cleanup on script exit
cleanup() {
    echo -e "\n🛑 Stopping Guardia Bot services..."
    if [ -n "${BACKEND_PID}" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    exit 0
}

# Catch Ctrl+C (SIGINT) and termination signals
trap cleanup SIGINT SIGTERM

echo "Starting FastAPI Backend on http://localhost:8000..."
uvicorn app.main:app --reload &
BACKEND_PID=$!

echo "Starting Streamlit Frontend on http://localhost:8501..."
streamlit run frontend/streamlit_app.py

# Wait for background processes
wait $BACKEND_PID
