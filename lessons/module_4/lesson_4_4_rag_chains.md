# Lesson 4.4: Simple RAG Chains

*Teaching the Agent New Facts*

## Introduction

LLMs are frozen in time. They don't know about the orders placed 5 minutes ago or the new laptop added to your store yesterday. **RAG** (Retrieval Augmented Generation) is the solution. It allows the agent to "look up" facts before answering.

---

## 1. What is RAG?

RAG follows a simple 3-step process:

1. **Retrieve**: When the user asks a question, the system searches a data source (like a database or document store) for relevant info.
2. **Augment**: The retrieved info is added to the system prompt.
3. **Generate**: The LLM answers the question using its retrieved "cheat sheet."

---

## 2. SQL as a Retrieval Source

While many people think RAG requires a "Vector Database," any data source can be used. In our project, we use **SQL-based RAG**.

**In our code (`backend/src/agents/product_agent.py`):**

1. **Retrieve**: We call `db_search_products(query="laptop")`.
2. **Augment**: The tool result (a list of laptops) is sent to the LLM.
3. **Generate**: The LLM recommends the specific laptops found in our database.

---

## 3. The LangChain RAG Pattern

In more complex systems, LangChain uses a **Retriever** object. A typical RAG chain looks like this:

```python
# A common LangChain RAG chain
chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```

---

## 🛠️ In Our Project: The Product Agent

Our **Product Agent** is a perfect example of a RAG agent. It doesn't rely on Gemini's general knowledge of laptops. Instead, it uses a specialized tool to fetch *our specific products* and *our specific reviews* before answering the customer.

This ensures the agent never recommends a product we don't actually sell!

---

## Summary

RAG is the key to building agents that are grounded in reality. By combining the reasoning of an LLM with the precision of a database, you create a system that is both smart and accurate.

> [!TIP]
> **Grounding**: RAG is often called "Grounding" because it keeps the AI's feet on the ground—preventing it from "hallucinating" facts that aren't in your data.
