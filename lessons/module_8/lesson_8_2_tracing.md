# Lesson 8.2: Performance Tracing

*Seeing Inside the Machine*

## Introduction

When a multi-agent system fails, it's often hard to see why. Did the Supervisor route it wrong? Did the tool return bad data? **Tracing** provides a step-by-step "log" of exactly what happened at every second of the conversation.

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

## 2. Industry Tools (LangSmith)

The most popular tool for this is **LangSmith**. It automatically records every part of your LangChain or LangGraph flow.

**What you see in a trace**:

- The exact **System Prompt** used.
- The raw **JSON** from the model.
- The **Latency** (how long it took) of each node.
- The **Cost** (number of tokens) for each call.

---

## 🛠️ In Our Project: Terminal Logs

Since we are building this locally, we use **Terminal Logs** as our simple tracing tool.

**In the terminal (`docker` logs):**
You can see lines like:
`INFO:src.graph:Supervisor decided to route to: order_agent`
`INFO:httpx:HTTP Request: POST ... gemini ... 200 OK`

These logs are "Mini-Traces" that help us debug when the agents act unexpectedly.

---

## Summary

Tracing is the "X-ray" of the AI world. Without it, you are guessing. With it, you can pinpoint exactly which part of your agent team is underperforming and fix it.

> [!TIP]
> **Production Rule**: Never run an agent in production without tracing active. One bad loop can cost a lot of money and frustrate your users—tracing is your first line of defense.
