# Lesson 4.5: Vector Databases and Chunking

*Giving the Agent Long-Term Contextual Memory*

## 1. What is a Vector Database?

Traditional databases (like PostgreSQL) are great at finding exact matches. If you search for "Titan Laptop", it looks for those exact characters.

However, LLMs think in **Vectors** (mathematical numbers representing meaning). A **Vector Database** allows us to perform "Similarity Search."

- **Embedding**: Converting text into a list of numbers (a vector).
- **Similarity**: Finding vectors that are "close" in mathematical space.

Example: A vector for "Great battery life" would be very close to "Lasts all day!", even though they share no common words.

---

---

## 2. How Data is Structured

In ChromaDB, each entry is a **Document** with three essential components:

### A. Page Content (The "Searchable" Text)

This is what the embedding model "reads" to understand meaning.

```text
Product: Titan ProBook 15
Rating: 5/5
Review: The battery life is incredible. I got 12 hours of solid development time!
```

### B. Metadata (The "Labels")

Keys and values used for filtering or quick reference.

```json
{
  "product_id": "prod_001",
  "rating": 5,
  "product_name": "Titan ProBook 15"
}
```

### C. The Embedding (The "Mathematical" Format)

A hidden list of numbers (the vector) that allows for similarity search.
*Example*: `[0.12, -0.04, 0.89, ...]`

---

## 3. Internal Database View (Real Example)

If you were to peek inside our actual ChromaDB after seeding, a single **row** looks exactly like this:

| Field | Value |
| :--- | :--- |
| **ID** | `17d7b2c2-547c-4e0e-bb8a-b41d2b6544b5` |
| **Embedding** | `[-0.0025, 0.0095, 0.0041, -0.0807, ...]` (3072 numbers total) |
| **Metadata** | `{"product_id": "P001", "product_name": "ProBook Laptop 15", "rating": 5}` |
| **Document** | `"Product: ProBook Laptop 15\nRating: 5/5\nReview: Incredible performance..."` |

### Keys to notice

1. **The Vector is a "Mathematical Map"**: Every decimal in that list represents a specific "feature" of the text that Gemini detected (e.g., tone, subject, sentiment).
2. **Metadata is your Filter**: We can tell the database to "only search vectors where `product_id` is X."
3. **The ID is the Link**: This UUID connects the numbers to the actual text safely.

---

## 4. Chunking Methods

You can't usually feed a 500-page manual into an LLM all at once (due to context limits). **Chunking** is the process of breaking large text into smaller, digestible pieces.

### Common Chunking Strategies

1. **Fixed-size Chunking**: Breaking text every X characters. Simple, but might cut off a sentence in the middle.
2. **Recursive Character Chunking**: Breaks at logical points like paragraphs (`\n\n`), then sentences (`.`), then words. This keeps context intact.
3. **Semantic Chunking**: Using an LLM to decide where the topic changes and breaking there.

---

## 4. Implementing Chunking in Our Project

In the real world, documents like "Terms and Conditions" or "User Manuals" are too big for a single vector. We use **Recursive Character Chunking** to split them logically.

Even though our product reviews are short, we've implemented chunking in `backend/src/db/seed_vector_db.py` to show you how it works:

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=150,    # Max characters per chunk
    chunk_overlap=20,  # Keep 20 chars from the previous chunk for context
    separators=["\n\n", "\n", ".", " ", ""] # Try to split at these points in order
)

# This creates multiple Document objects for one long review
chunks = text_splitter.split_text(full_review_text)
```

### Why use Overlap?

If a sentence is cut in half, the AI loses context. By keeping a small **overlap**, we ensure that the "meaning" of the ending of chunk 1 is carried over into the beginning of chunk 2.

---

## 5. 🛠️ In Our Project: ChromaDB

We use **ChromaDB** to store and search through thousands of product reviews.

**Implementation Example** (`backend/src/db/vector_store.py`):

```python
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

db = Chroma(
    collection_name="product_reviews",
    embedding_function=GoogleGenerativeAIEmbeddings(model="models/embedding-001"),
    persist_directory="./chroma_db"
)

# Search for reviews based on meaning
results = db.similarity_search("How is the keyboard on the Titan?")
```

### Why we use this for RAG?

When a user asks: *"Are people happy with the Titan laptop?"*

1. We search the Vector DB for "Titan laptop reviews".
2. We retrieve the top 5 most relevant reviews.
3. we feed those reviews into the LLM as "Context".
4. The LLM answers based on real customer feedback.

---

## 🚀 Hands-on: Seed the Vector DB

In our modern Docker stack, **seeding is automatic!** When you run `docker-compose up`, a dedicated `seeder` service handles this for you.

### How to Force a Re-seed (Docker)

If you modify the source data or want a fresh start while Docker is running:

```bash
# Seed SQL Database
docker-compose exec backend python3 src/db/seed_db.py

# Seed Vector Database
docker-compose exec backend python3 src/db/seed_vector_db.py
```

### Local Fallback (No Docker)

If you are running scripts directly on your machine:

```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/backend
python3 backend/src/db/seed_vector_db.py
```

---

## Summary

Vector databases are the foundation of **Retrieval-Augmented Generation (RAG)**. They allow agents to "know" things that weren't in their original training data by looking them up in real-time.
