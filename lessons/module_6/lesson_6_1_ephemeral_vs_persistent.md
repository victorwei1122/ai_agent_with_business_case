# Lesson 6.1: Ephemeral vs. Persistent Memory

*Don't Let Your Agent Forget*

## Introduction

An LLM is naturally "stateless." It has no idea what you said 30 seconds ago unless you send that information back to it. In agent-speak, we divide memory into two types: **Ephemeral** and **Persistent**.

---

## 1. Ephemeral Memory (Short-Term)

Short-term memory exists only during a single "Session." If you close your browser or refresh the page, the memory is deleted.

- **How it works**: We keep the `messages` list in a local variable in our code.
- **Benefit**: Extremely fast and requires no database.

---

## 2. Persistent Memory (Long-Term)

Long-term memory allows the agent to recognize you even if you come back a week later. It saves the **State** to a permanent database.

- **How it works**: We use a **Checkpointer**.
- **Benefit**: Essential for customer support, where users might resume a conversation later.

---

## 🛠️ In Our Project: The Checkpointer

In our project's `graph.py`, we use LangGraph's checkpointer system.

```python
from langgraph.checkpoint.memory import MemorySaver

# We initialize a checkpointer
checkpointer = MemorySaver()

# We compile our graph with it
app_graph = workflow.compile(checkpointer=checkpointer)
```

By adding this one line, our agent gains the ability to save every "Thought" and "Observation" it has ever had.

---

## 3. The "Thread" Concept

Memory is organized by **Threads**.

- A **Thread ID** is like a unique ID for a specific conversation.
- If Customer A and Customer B both talk to the bot, they have different Thread IDs.
- The bot remembers what Customer A said *only* when talking to Customer A.

---

## Summary

Memory turns a one-off tool into a helpful assistant. By understanding the difference between short-term ephemeral memory and long-term persistence, you can design agents that build real relationships with users.

> [!NOTE]
> In our project, we use `MemorySaver` (in-memory), but in a real production app, you would swap this out for a `PostgresSaver` or `SqliteSaver` to ensure data survives a server restart.
