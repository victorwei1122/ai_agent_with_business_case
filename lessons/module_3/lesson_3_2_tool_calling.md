# Lesson 3.2: Tool Calling & Function Binding

*Connecting the Brain to the Hands*

## Introduction

An LLM by itself is just a "brain in a jar." It can talk about the world, but it can't change it. **Tool Calling** (also known as Function Calling) is the process of giving the AI a set of "remote controls" it can use to interact with your code, database, or external APIs.

---

## 1. The "@tool" Pattern

In modern frameworks like LangChain, we don't just write a function; we decorate it with `@tool`. This tells the system that this function is available for the LLM to call.

**In our code (`backend/src/agents/order_agent.py`):**

```python
@tool
def db_lookup_order(order_id: str) -> Dict[str, Any]:
    """Look up an order by its ID. Returns order status, items, tracking info, and dates."""
    # ... logic to query SQL database ...
```

---

## 2. Function Binding: The "Sales Pitch"

The LLM doesn't see your Python code. It sees a specialized JSON description of your function. When we "bind" tools to an LLM, we send it a schema that looks like this:

**What the AI actually sees:**

```json
{
  "name": "db_lookup_order",
  "name_in_context": "db_lookup_order",
  "description": "Look up an order by its ID. Returns order status, items, tracking info, and dates.",
  "parameters": {
    "type": "object",
    "properties": {
      "order_id": {
        "title": "Order Id",
        "type": "string"
      }
    },
    "required": ["order_id"]
  }
}
```

In simpler terms, the agent sees:

- **Name**: `db_lookup_order`
- **Description**: "Look up an order by its ID. Returns order status..."
- **Arguments**: `order_id` (Type: string)

### Docstrings are Code

Notice how the `description` comes directly from your function's **docstring**, and the `type` comes from your **type hints** (`order_id: str`). In agent development, your documentation is actually part of your logic—if you write a poor description, the AI will use the tool incorrectly.

---

## 🛠️ In Our Project: Multi-Tool Agents

An agent becomes powerful when it has a broad "Toolbox."

Our **Order Agent** has three main tools:

1. `db_lookup_order`: For finding specific facts.
2. `db_process_refund`: For taking actions that change state.
3. `db_get_sales_analytics`: For high-level reasoning across many records.

When the LLM receives a query, it selects the **Right Tool for the Job** based on the descriptions we wrote in the docstrings.

### What if no tool fits?

If the user asks something that doesn't match any tool description (e.g., "What's the weather like?"), the AI simply won't call a tool. Instead, it will:

1. **Skip the Tool Call**: The `response.tool_calls` list will be empty.
2. **Fallback to Conversation**: The agent will generate a normal text response (e.g., "I'm sorry, I only have access to order and sales data, not weather info.").
3. **Exit the Loop**: Since no tool was called, the `for` loop finishes and returns the text to the user.

---

## 3. Handling Arguments: The Pydantic Shield

One of the hardest parts of tool calling is ensuring the AI provides the right arguments. If the AI sends a number when we expect a string, our code will crash.

We use **Structured Validation** (using Pydantic) to ensure the agent's inputs are clean.

**In our code (`backend/src/agents/llm_utils.py`):**
We implemented `clean_tool_args` to specifically handle cases where the AI sends empty values or improperly formatted JSON. This acts as a "shield" between the AI and our database.

---

## Summary

Tool calling turns an AI from a respondent into a participant. By defining clear tools and binding them to the LLM, you enable the agent to solve real business problems using live data.

> [!IMPORTANT]
> **Docstrings are Code**: In tool calling, your documentation (the docstring) is part of the logic. If you write a poor description, the AI will use the tool incorrectly. Always be clear about *when* and *why* a tool should be used.
