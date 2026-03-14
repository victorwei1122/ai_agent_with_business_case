# Lesson 8.2: Performance Tracing & Observability

*Seeing Inside the Machine with LangSmith*

## Introduction

When a multi-agent system fails, it's often hard to see why. Did the Supervisor route it wrong? Did the tool return bad data? **Tracing** provides a step-by-step "log" of exactly what happened at every second of the conversation.

In this lesson, we move beyond simple print statements to professional observability using **LangSmith**.

---

## 1. The "Black Box" Problem

In a normal LLM call, you send text and get text. But in our system:

1. **Supervisor** thinks (Invisible).
2. **Supervisor** routes (Invisible).
3. **Agent** thinks (Invisible).
4. **Tool** runs (Visible in database).
5. **Agent** responds (Visible).

Tracing makes all those middle steps visible.

---

## 2. Professional Tracing: LangSmith

[LangSmith](https://smith.langchain.com/) is a platform for building production-grade LLM applications. It allows you to debug, test, evaluate, and monitor chains and intelligent agents built on any LLM framework.

### Why use LangSmith?

- **Visual Debugging**: See the exact sequence of events in a graph or tree view.
- **Prompt Inspection**: View the exact system and user prompts sent to the model (after all variables are injected).
- **Latency Analysis**: Identify which step is slowing down your agent.
- **Cost Tracking**: Monitor token usage across different models and runs.
- **Dataset Creation**: Easily turn traces into testing datasets for future evaluations.

---

## 3. Setting Up LangSmith

To enable tracing in our project, you only need to set a few environment variables. No code changes are typically required if you are using LangChain or LangGraph.

### Step 1: Get an API Key

Sign up at [smith.langchain.com](https://smith.langchain.com/) and create a new API key in the settings.

### Step 2: Configure Environment Variables

Add these to your `.env` file or export them in your terminal:

```bash
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY="ls__..."
export LANGCHAIN_PROJECT="ai-agent-tutorial" # Optional: Give your project a name
```

---

## 4. Reading a Trace

When you open a trace in LangSmith, you'll see a hierarchy of "Runs":

1. **The Root Run**: The overall entry point (e.g., your LangGraph app).
2. **Child Runs**: Individual nodes (Supervisor, Order Agent, etc.).
3. **Grandchild Runs**: Tool calls or specific LLM invocations.

### What to look for

- **Inputs/Outputs**: Are they what you expected? If a tool failed, was it because of the input it received?
- **Metadata**: See the model version, temperature, and other config used for that specific call.
- **Error Logs**: If a run failed, the stack trace is captured directly in the UI.

---

## 🛠️ Tracing in Our Project

In our e-commerce project, tracing allows us to answer questions like:

- *"Why did the Supervisor send this request to the Order Agent instead of the Product Agent?"*
- *"What exact SQL query did the `search_products` tool generate?"*

### Comparison: Terminal vs. LangSmith

| Feature | Terminal Logs | LangSmith |
| :--- | :--- | :--- |
| **Readability** | Hard (scrolling text) | Easy (collapsible tree) |
| **Prompt Depth** | Limited | Full System + User view |
| **History** | Gone when terminal closes | Persistent and searchable |
| **Collaboration** | None | Shareable links for teams |

---

## Summary

Tracing is the "X-ray" of the AI world. Without it, you are guessing. With it, you can pinpoint exactly which part of your agent team is underperforming and fix it.

> [!TIP]
> **Production Rule**: Never run an agent in production without tracing active. One bad loop can cost a lot of money and frustrate your users—tracing is your first line of defense.
