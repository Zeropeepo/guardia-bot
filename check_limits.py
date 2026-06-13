import os
import requests
from dotenv import load_dotenv

load_dotenv()

def print_limits(name, resp):
    print(f"\n{'='*40}")
    print(f"{name} API")
    print(f"{'='*40}")
    print(f"HTTP Status Code: {resp.status_code}")
    
    if resp.status_code != 200:
        print(f"Error Response: {resp.text}")
        return

    # Filter headers for rate limit info
    limit_headers = {k: v for k, v in resp.headers.items() if 'ratelimit' in k.lower() or 'limit' in k.lower()}
    
    if limit_headers:
        print("\nRate Limit Information:")
        for k, v in limit_headers.items():
            print(f"  {k}: {v}")
    else:
        print("\nNo rate limit headers found in the response.")

def check_groq():
    api_key = os.getenv("GROQ_API_KEY")
    model = os.getenv("GROQ_MODEL_NAME", "llama-3.1-8b-instant")
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}", 
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": "ping"}],
        "max_tokens": 5
    }
    
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=10)
        print_limits("Groq LLM", resp)
    except Exception as e:
        print(f"\nFailed to connect to Groq: {e}")

def check_jina_embeddings():
    api_key = os.getenv("JINA_API_KEY")
    url = "https://api.jina.ai/v1/embeddings"
    
    headers = {
        "Authorization": f"Bearer {api_key}", 
        "Content-Type": "application/json"
    }
    data = {
        "model": "jina-embeddings-v3", 
        "input": ["ping"]
    }
    
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=10)
        print_limits("Jina Embeddings", resp)
    except Exception as e:
        print(f"\nFailed to connect to Jina Embeddings: {e}")

def check_jina_reranker():
    api_key = os.getenv("JINA_API_KEY")
    url = "https://api.jina.ai/v1/rerank"
    
    headers = {
        "Authorization": f"Bearer {api_key}", 
        "Content-Type": "application/json"
    }
    data = {
        "model": "jina-reranker-v2-base-multilingual", 
        "query": "ping",
        "documents": ["pong"]
    }
    
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=10)
        print_limits("Jina Reranker", resp)
    except Exception as e:
        print(f"\nFailed to connect to Jina Reranker: {e}")

def check_mimo():
    api_key = os.getenv("MIMO_API_KEY")
    base_url = os.getenv("MIMO_BASE_URL", "https://api.mimo.ai/v1").rstrip("/")
    model = os.getenv("MIMO_MODEL_NAME", "mimo-text-model")
    url = f"{base_url}/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}", 
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": "ping"}],
        "max_tokens": 5
    }
    
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=10)
        print_limits("Mimo LLM", resp)
    except Exception as e:
        print(f"\nFailed to connect to Mimo: {e}")

if __name__ == "__main__":
    print("Fetching API Limits from Providers...\n")
    check_groq()
    check_jina_embeddings()
    check_jina_reranker()
    check_mimo()
