import os
import yaml
from typing import List, Dict, Any
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.tools import tool
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Path to persistent ChromaDB storage
CHROMA_PATH = os.path.join(os.path.dirname(__file__), "../../chroma_db")

def find_config():
    """Find config.yml in common locations."""
    # Look for config.yml relative to this file first
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) # Project root
    paths = [
        os.path.join(base_dir, "backend/config.yml"),
        os.path.join(base_dir, "config.yml"),
        "config.yml",
        "backend/config.yml"
    ]
    for path in paths:
        if os.path.exists(path):
            with open(path, "r") as f:
                return yaml.safe_load(f) or {}
    return {}

def get_embeddings():
    """Initialize embeddings using API key from config.yml or environment."""
    config = find_config()
            
    api_key = config.get("gemini_api_key") or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Gemini API key not found for embeddings. Set it in config.yml or as GEMINI_API_KEY environment variable.")
        
    return GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key=api_key)

def get_vector_store():
    """Initialize or load the Chroma vector store. Supports local and server mode."""
    embeddings = get_embeddings()
    
    server_host = os.getenv("CHROMA_SERVER_HOST")
    server_port = os.getenv("CHROMA_SERVER_HTTP_PORT", "8000")
    
    if server_host:
        import chromadb
        from langchain_chroma import Chroma
        
        client = chromadb.HttpClient(host=server_host, port=int(server_port))
        return Chroma(
            client=client,
            collection_name="product_reviews",
            embedding_function=embeddings
        )
    else:
        # Local Persistent Mode (Default)
        return Chroma(
            collection_name="product_reviews",
            embedding_function=embeddings,
            persist_directory=CHROMA_PATH
        )

def search_reviews(query: str, n_results: int = 5) -> List[Dict[str, Any]]:
    """Search for relevant product reviews using similarity search."""
    db = get_vector_store()
    results = db.similarity_search(query, k=n_results)
    
    return [
        {
            "content": doc.page_content,
            "metadata": doc.metadata
        }
        for doc in results
    ]

@tool
def vec_search_reviews(query: str) -> Dict[str, Any]:
    """
    Search all product reviews for specific sentiments, features, or issues using natural language.
    Use this when a user asks 'What do people think about X?' or 'Are there any issues with Y?'.
    Returns the most relevant reviews across the entire platform.
    """
    try:
        results = search_reviews(query)
        return {
            "success": True,
            "results": results
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
