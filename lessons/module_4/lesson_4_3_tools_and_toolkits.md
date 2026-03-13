# Lesson 4.3: Tools and Toolkits

*Giving the Agent Specialized Skills*

## Introduction

In LangChain, a **Tool** is not just a function—it's a standardized interface that allows any LLM to understand how to interact with your code. When you group multiple tools together, you create a **Toolkit**.

---

## 1. Defining a Tool

LangChain provides the `@tool` decorator, which automatically turns a Python function into a tool the AI can use.

The most important part of a tool is its **Type Hints** and **Docstrings**. LangChain uses these to generate the JSON schema that is sent to the LLM.

**In our code (`backend/src/agents/order_agent.py`):**

```python
@tool
def db_lookup_order(order_id: str) -> Dict[str, Any]:
    """Look up an order by its ID. Returns status and tracking..."""
```

- **The Name**: `db_lookup_order`
- **The Type Hint**: `order_id: str` (The AI knows it must provide a string)
- **The Docstring**: Tells the AI *when* to use this tool.

---

## 2. Structured Tools

Sometimes a tool needs complex inputs (like an object with many fields). LangChain supports this via Pydantic models.

**Example**: If we wanted to create a tool for creating a complex support ticket, we would define a Pydantic class:

```python
class TicketSchema(BaseModel):
    subject: str
    priority: str
    description: str

@tool(args_schema=TicketSchema)
def create_ticket(args: TicketSchema):
    ...
```

---

## 🛠️ In Our Project: The `order_tools` List

We group our related tools into a list. This is essentially our "Order Toolkit."

```python
order_tools = [db_lookup_order, db_process_refund, db_get_sales_analytics]
```

When we call `.bind_tools(order_tools)`, the LLM is given the instructions for all three skills at once. It chooses between them based on the descriptions we wrote.

---

## 3. Toolkits

LangChain also provides pre-built **Toolkits** for common tasks:

- **SQLDatabaseToolkit**: Allows an agent to safely query a database.
- **GmailToolkit**: Allows an agent to read/write emails.
- **SearchTool**: Connects an agent to Google or DuckDuckGo.

---

## Summary

Tools are how we extend an LLM's knowledge and actions. By standardizing these skills into tools, we can reuse them across different agents and projects.

> [!IMPORTANT]
> **Safety First**: Tools are powerful. Always ensure your tools have "Guardrails"—like checking permissions or limiting results—before exposing them to an AI.
