# Lesson 0.2: What is an Agent?

*From Assistants to Autonomous Workers*

## Introduction

If an LLM (Large Language Model) is a "Brain," an **AI Agent** is the "Body" that uses that brain to get things done.

Most people use AI as an **Assistant** (they ask a question, and it answers). But we are building **Agents**, which are fundamentally different.

---

## 1. Assistant vs. Agent: The Key Difference

| Feature | AI Assistant (Chatbot) | AI Agent |
| :--- | :--- | :--- |
| **Logic** | Linear (Q & A) | Cyclical (Iterative) |
| **Ownership** | You do the work; it helps. | It does the work for you. |
| **Tools** | Can't "touch" anything outside the chat. | Can use APIs, browse the web, and edit databases. |
| **Autonomy** | Needs step-by-step guidance. | Needs a goal (it decides the steps). |

---

## 2. The Agentic Loop

The core of every AI Agent is a loop called **Reasoning**. It follows these steps:

1. **Plan**: The agent looks at the goal and thinks, "What do I need to do first?"
2. **Act**: The agent performs an action (like calling a search tool).
3. **Observe**: The agent looks at the result of that action (e.g., "The search found 3 products").
4. **Refine**: Based on the observation, it updates its plan and continues the loop until the task is done.

---

## 3. The 4 Pillars of an AI Agent

To be a truly "agentic" system, an agent needs four things:

### A. The Browser (LLM)

The reasoning engine that interprets the user's intent.

### B. Planning

The ability to break down complex tasks into smaller, manageable steps.

### C. Tools (Function Calling)

The ability to interact with the external world (e.g., checking an order status in a SQL database).

### D. Memory

The ability to remember what it has already tried and what the user has said previously.

---

## 🛠️ In Our Project: Meet the Agents

Our e-commerce system is powered by three distinct "agentic" entities:

1. **[Product Agent](../../backend/src/agents/product_agent.py)**: Specialized in finding products and reading reviews.
2. **[Order Agent](../../backend/src/agents/order_agent.py)**: Specialized in checking order status and sales analytics.
3. **[Supervisor](../../backend/src/graph.py)**: The "Manager" agent that decides which specialist should handle your request.

---

## Summary

An Agent doesn't just talk; it **does**. It moves through the world by planning, acting, and learning from its results.

> [!IMPORTANT]
> **The Golden Rule of Agents**: An agent is defined not by its IQ, but by its **agency**—its ability to take actions in pursuit of a goal.
