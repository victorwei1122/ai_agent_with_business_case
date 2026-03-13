# Lesson 7.1: Conditional Edges

*Handling the Unexpected*

## Introduction

In a perfect world, an agent always makes the right choice. In reality, tools fail, LLMs hallucinate, and users ask nonsensical questions. **Conditional Edges** are how we build safety nets into our agent's brain.

---

## 1. Beyond the Happy Path

A "Happy Path" is when everything goes right. A "Conditional Edge" allows you to define a "Sad Path" or "Retry Path."

**Example Logic**:

- IF the Product Agent found results → Go to **Response**.
- ELSE IF the Product Agent failed → Go to **Retry** or **Human Escalation**.

---

## 2. Dynamic Routing based on Content

You can write a function that looks at the *text* of an agent's response to decide the next edge.

**In our code (`backend/src/graph.py`):**

```python
def route_after_agent(state: AgentState):
    # If the response contains an error message, route to a help node
    if "Error" in state["messages"][-1].content:
        return "help_node"
    return "supervisor"
```

---

## 🛠️ In Our Project: The `FINISH` route

Our most important conditional edge is handled by the Supervisor. It looks at the conversation and decides if the task is finished.

```python
# The mapping for our conditional edge
{
    "product_agent": "product_node",
    "order_agent": "order_node",
    "FINISH": END # The 'END' node is a special LangGraph constant
}
```

By allowing the AI to choose `FINISH`, we enable the agent to stop talking when the user is satisfied.

---

## Summary

Conditional edges are the "If/Then" statements of the agent world. They provide the flexibility needed to handle complex business logic and unexpected errors without breaking the entire system.

> [!TIP]
> **Defensive Design**: Always include a "Fallback" route in your conditional edges. If the LLM returns an unexpected string, your code should have a safe default (like returning to the Supervisor or Ending).
