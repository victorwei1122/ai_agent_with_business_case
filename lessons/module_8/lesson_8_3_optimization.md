# Lesson 8.3: Cost & Latency Optimization

*Faster and Cheaper Agents*

## Introduction

AI agents can be expensive and slow. Every "Step" in a graph costs money and takes time. In production, your job is to make the agent as efficient as possible without losing accuracy.

---

## 1. Choosing the Right Model

Not every job needs a "Super-Model" like GPT-4o or Gemini Ultra.

- **Small Models (e.g., Gemini Flash)**: Fast and cheap. Great for routing, summarization, and simple tool calling.
- **Large Models (e.g., Gemini Pro)**: Slower and more expensive. Use these for complex reasoning or highly sensitive data.

---

## 🛠️ In Our Project: Gemini Flash

We explicitly chose **Gemini Flash** for this project.

- **Why?**: It is incredibly fast (low latency), which makes the chatbot feel modern and responsive.
- **Efficiency**: It is capable of tool calling and following structured instructions while being a fraction of the cost of larger models.

---

## 2. Reducing Token Waste

Every word you send to an LLM costs money. You can optimize this by:

- **Concise System Prompts**: Don't repeat yourself.
- **Trimming History**: Only send the relevant parts of the conversation.
- **Lower Temperature**: As we learned in **Module 1**, Temperature 0 (Deterministic) often reduces extra "chatter" and saves tokens.

---

## 3. Parallel Execution

In LangGraph, you can run multiple nodes at once. If you need two agents to work on different parts of a problem, running them in parallel reduces the total time the user has to wait.

---

## Conclusion

Optimization is an ongoing process. As you monitor your agent's traces and evaluation scores, you will find places where you can save money and improve speed.

> [!TIP]
> **The 80/20 Rule**: Usually, 80% of your agent's work can be done by a small, fast model. Reserve the large, slow models only for the critical 20% of complex decisions.
