# Lesson 5.1: State Management

*What the Agent Knows and Carries*

## Introduction

In a complex system, an AI doesn't just "answer a message." It often moves through a series of steps. **LangGraph** uses a concept called **State** to keep track of everything that has happened so far.

---

## 1. The State Object

Think of the State as a "shared notepad." Every agent in the graph can read from it and write to it. In LangGraph, we define this structure using a Python dictionary or a TypedDict.

**In our code (`backend/src/graph.py`):**

```python
class AgentState(TypedDict):
    # The history of the entire conversation
    messages: Annotated[Sequence[BaseMessage], operator.add]
    # Where to route the next message
    next: str
    # Information about the user
    user_info: Dict
```

---

## 2. Reducers: How State Changes

In the code above, `operator.add` is a **Reducer**. It tells LangGraph: "When a new message is created, don't delete the old ones—just *add* the new one to the list."

This ensures that our agents always have access to the full conversation history.

---

## 🛠️ In Our Project: The `State` flow

When you ask our bot a question, here is what happens to the State:

1. **User Message**: A `HumanMessage` is added to the `messages` list in the State.
2. **Supervisor**: Reads the `messages`, decides the next step, and updates the `next` field in the State.
3. **Specialized Agent**: Reads the State, calls a tool, and adds a `ToolMessage` and an `AssistantMessage` to the `messages` list.

---

## 3. Why State Matters

Without state, we could never build agents that work together. One agent would have no idea what the last agent did. State acts as the **Short-Term Memory** of our system.

---

## Summary

State is the "single source of truth" for your agent. By managing state correctly, you can build reliable workflows where multi-step logic and complex handovers between agents are possible.

> [!TIP]
> **Minimalism is Key**: Only put information in the State that *multiple* parts of your graph need to know. If an agent has a secret calculation, keep it inside the agent's function!
