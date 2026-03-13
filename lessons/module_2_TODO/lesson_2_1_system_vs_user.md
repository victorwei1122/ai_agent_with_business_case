# Lesson 2.1: System vs. User Messages

*Defining the AI's Identity*

## Introduction

When communicating with an LLM in a production agent, we don't just send the user's question. We send a conversation history that is divided into different "roles." The two most important roles are the **System Message** and the **User Message**.

---

## 1. The System Message: The "Rules of the Game"

The System Message is a hidden instruction that sets the stage for the entire conversation. It tells the AI:

- **Who it is** (Identity/Persona).
- **What it can do** (Capabilities).
- **What it cannot do** (Boundaries).
- **How it should talk** (Tone/Style).

Think of the System Message as the "Employee Handbook" that the AI reads before it ever meets the customer.

---

## 2. The User Message: The "Request"

The User Message is the actual text typed by the person using the app. It is the specific problem or question the AI needs to solve *within the rules set by the System Message*.

---

## 🛠️ In Our Project: Specialized Personas

We use different System Messages to turn the same LLM into three different experts.

### Product Agent Persona

In `backend/src/agents/product_agent.py`, we define a persona focused on sales:

```python
SystemMessage(content="You are the specialized Product Agent. You help customers find laptops, headphones, and other items. You do NOT look up orders.")
```

### Order Agent Persona

In `backend/src/agents/order_agent.py`, we define a persona focused on data and accuracy:

```python
SystemMessage(content="You are the specialized Order Agent. You help customers track orders and process refunds. You do NOT directly recommend products.")
```

### Why split them?

If we gave one agent *all* the instructions, it would become confused and likely to make mistakes. By using specific System Messages, we ensure the agent stays focused on its job.

---

## 3. Best Practices for System Messages

- **Be Explicit**: Don't say "Be helpful." Say "Be helpful, concise, and never mention our competitors."
- **Use Order of Importance**: Models often pay more attention to the beginning and end of the message.
- **Set Boundaries**: Always tell the agent what it *shouldn't* do to prevent it from going off track.

---

## Summary

The System Message is your primary lever for controlling agent behavior. It defines the "Soul" of the agent, while the User Message provides the "Source" of the work.

> [!TIP]
> A well-written System Message is like a well-written job description. If it's vague, the worker (the AI) will be unpredictable.
