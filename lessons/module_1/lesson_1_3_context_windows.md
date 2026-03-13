# Lesson 1.3: Context Windows and Attention

*Managing the AI's Short-Term Memory*

## Introduction

Every AI model has a limit to how much information it can "think about" at one time. This limit is called the **Context Window**.

---

## 1. What is a Context Window?

Think of the Context Window as the "RAM" or "Desktop space" for the AI.

- Everything in the current conversation (the history, the system prompt, and any search results) must fit inside this window.
- If you exceed the window, the model "forgets" the earlier parts of the conversation.

**Window Sizes**:

- Gemini Flash: ~1 Million Tokens (Massive)
- Older models: 8k - 32k Tokens (Small)

---

## 2. Why Attention Matters

"Attention" is the mechanism the model uses to decide which parts of the context window are most relevant right now.

Even with a 1-million-token window, if a model has to look through 500 pages of text to find one specific order number, its performance might degrade. This is known as the **"Lost in the Middle"** problem—models are best at remembering the very beginning and the very end of their context.

---

## 🛠️ In Our Project: The Scalability Challenge

Imagine our e-commerce business grows to **10,000 customers** and **50,000 orders**.

If we simply shoved every order into the system prompt, we would:

1. Exceed the context window (even Gemini's).
2. Make the agent very slow (more tokens = more latency).
3. Waste money (more tokens = higher cost).

### The Solution: Targeted Queries

Instead of giving the agent *all* the data, we give it **Tools**.

- In `backend/src/agents/order_agent.py`, the agent uses a SQL query to fetch *only* the specific order it needs.
- By fetching only relevant information, we keep the context window clean and the agent fast.

---

## Summary

The context window is the limit of the AI's immediate awareness. Professional agent design is about managing this window efficiently by only providing the information necessary for the current step.

> [!NOTE]
> **RAG (Retrieval Augmented Generation)** is the industry-standard way to solve context window limits. We'll cover this in Module 4!
