# Lesson 2.4: Structured Output

*Talking in JSON*

## Introduction

While LLMs are great at writing poetry and emails, agents need something more precise. To build a system where one agent can talk to another, or where an AI can trigger a UI change, we need **Structured Output** (usually JSON).

---

## 1. Why JSON?

Computers cannot reliably "read" a paragraph to find an order number. They need keys and values.

- **Unstructured**: *"The user wants to buy the SoundMax headphones. Route them to the product agent."*
- **Structured**: `{"route": "product_agent", "item": "SoundMax"}`

By forcing the AI to speak in JSON, we turn a "Chatter" into a "Program."

---

## 2. Techniques for Structured Output

### A. Instruction-Based (Prompting)

You simply tell the model to respond in JSON.

- **Example**: *"Respond only in JSON format with 'name' and 'age' keys."*
- **Risk**: The model might include markdown backticks (`` ```json ``) or extra text that breaks your code.

### B. JSON Mode

Many providers (like Google Gemini and OpenAI) have a specific "JSON Mode" setting that forces the model to guarantee a valid JSON response.

### C. Schema-Based (Pydantic)

This is the "Gold Standard." You define a Python class (a schema), and the AI is forced to fill in the fields of that class.

---

## 🛠️ In Our Project: The Supervisor and Tools

We use structured output in two critical places:

### 1. The Supervisor Routing

In `backend/src/graph.py`, our supervisor produces a JSON object so the code knows exactly which path to take:

```python
# The instruction in the system message
"Respond ONLY with a JSON object in this exact format: {'route': '<agent_name>'}"
```

### 2. Tool Calls

When an agent wants to search the database, it doesn't just "say" it. It generates a structured **Tool Call** that contains the function name and its arguments.

**In our code (`backend/src/agents/order_agent.py`):**
We use a function called `clean_tool_args` to ensure the JSON produced by the LLM is perfectly formatted before we use it to query our SQL database.

---

## Summary

Structured output is the bridge between AI reasoning and traditional software. Without it, agents are just chatbots; with it, they are powerful components of an automated system.

> [!CAUTION]
> **Always Validate**: Never trust that a model's JSON is perfect. Use a validation library (like Pydantic) or defensive code to handle cases where the model makes a typo in a key name.
