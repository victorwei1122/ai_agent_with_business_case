from typing import Dict, Any, Optional
import os
import yaml
from langchain_google_genai import ChatGoogleGenerativeAI
import logging

logger = logging.getLogger(__name__)

# Cache for LLM instances to avoid redundant initializations
_llm_cache = {}

def get_llm(model=None, temperature=0):
    """
    Helper to instantiate the LLM model (Gemini or Ollama),
    loading the provider and model preference from config.yml.
    Uses caching to avoid redundant initializations.
    """
    cache_key = f"{model}_{temperature}"
    if cache_key in _llm_cache:
        return _llm_cache[cache_key]

    try:
        config = {}
        if os.path.exists("config.yml"):
            with open("config.yml", "r") as f:
                config = yaml.safe_load(f) or {}
                
        provider = config.get("llm_provider", "gemini")
        
        if provider == "ollama":
            from langchain_ollama import ChatOllama
            target_model = config.get("ollama_model", "llama3.1:8b")
            base_url = config.get("ollama_base_url", "http://ollama:11434")
            # Increase timeout for slow local models and use a shared instance
            llm = ChatOllama(
                model=model or target_model, 
                temperature=temperature, 
                base_url=base_url,
                timeout=120, # 2 minute timeout for local generation
                num_ctx=4096 # Limit context to save memory
            )
        else:
            # Default to Gemini
            api_key = config.get("gemini_api_key") or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
            target_model = config.get("gemini_model", "gemini-flash-latest")
            
            if not api_key:
                raise ValueError("Gemini API key not found in environment or config.yml")
                
            llm = ChatGoogleGenerativeAI(model=model or target_model, temperature=temperature, google_api_key=api_key)
        
        _llm_cache[cache_key] = llm
        return llm
            
    except Exception as e:
        logger.error(f"LLM initialization error: {e}")
        if isinstance(e, ValueError): raise e
        # Minimal fallback if YAML fails
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("LLM initialization failed and no fallback API key found")
        llm = ChatGoogleGenerativeAI(model=model or "gemini-flash-latest", temperature=temperature, google_api_key=api_key)
        return llm

def get_text_content(response):
    """
    Extracts plain text content from a LangChain response.
    Handles both string content and list-of-dicts content (common with Gemini).
    """
    content = getattr(response, "content", response)
    if isinstance(content, list):
        # Extract text from the text parts
        return "".join([part["text"] for part in content if isinstance(part, dict) and "text" in part])
    return str(content)

def clean_tool_args(args: Any) -> Any:
    """
    Recursively cleans tool arguments.
    Ensures that empty dictionaries passed as field values are converted to None, 
    but keeps the root dictionary as a dictionary (even if empty) to satisfy 
    Pydantic's requirement for tool inputs.
    """
    if not isinstance(args, dict):
        return args
        
    cleaned = {}
    for k, v in args.items():
        if isinstance(v, dict) and not v:
            cleaned[k] = None
        elif isinstance(v, dict):
            cleaned[k] = clean_tool_args(v)
        elif isinstance(v, list):
            cleaned[k] = [clean_tool_args(i) if isinstance(i, dict) else i for i in v]
        else:
            cleaned[k] = v
    return cleaned
