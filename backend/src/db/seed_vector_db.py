import os
import sys

# Ensure backend root is in path
sys.path.append(os.path.join(os.path.join(os.path.dirname(__file__), ".."), ".."))

from src.db.database import SessionLocal
from src.db.models import ProductReview, Product
from src.db.vector_store import get_vector_store
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def seed_vector_db():
    """Extract reviews from SQLite, split into chunks, and ingest into ChromaDB."""
    db = SessionLocal()
    
    # Check if we're in server mode and wait for it
    server_host = os.getenv("CHROMA_SERVER_HOST")
    if server_host:
        print(f"Connecting to Chroma server at {server_host}...")
        import time
        import requests
        for _ in range(30):
            try:
                requests.get(f"http://{server_host}:8000/api/v1/heartbeat")
                break
            except:
                time.sleep(1)
    
    vector_store = get_vector_store()
    
    print("Fetching reviews from database...")
    reviews = db.query(ProductReview).all()
    
    # 1. Initialize the Text Splitter (Chunking Strategy)
    # We use a small chunk_size=150 to demonstrate splitting.
    # RecursiveCharacterTextSplitter is the industry standard for RAG.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=150,    # Max characters per chunk
        chunk_overlap=20,  # Context overlap for continuity
        separators=["\n\n", "\n", ".", " ", ""]
    )
    
    documents = []
    for review in reviews:
        # Get product name for context
        product_name = review.product.name if review.product else "Unknown Product"
        
        # Create a rich text representation
        full_text = f"Product: {product_name}\nRating: {review.rating}/5\nReview: {review.comment}"
        
        # 2. Apply the Chunking logic
        # This turns 1 long text into a list of smaller strings (chunks)
        chunks = text_splitter.split_text(full_text)
        
        for chunk in chunks:
            doc = Document(
                page_content=chunk,
                metadata={
                    "product_id": review.product_id,
                    "product_name": product_name,
                    "review_id": review.id,
                    "rating": review.rating
                }
            )
            documents.append(doc)
    
    if documents:
        print(f"Ingesting {len(documents)} logic chunks into ChromaDB...")
        
        # Clear existing data to avoid duplicates for the demo
        try:
            ids = vector_store.get()['ids']
            if ids:
                vector_store.delete(ids=ids)
        except Exception as e:
            print(f"Warning: Could not clear existing vectors: {e}")
            
        vector_store.add_documents(documents)
        print("Vector database seeding complete.")
    else:
        print("No reviews found in the database.")
    
    db.close()

if __name__ == "__main__":
    seed_vector_db()
