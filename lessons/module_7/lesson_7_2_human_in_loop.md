# Lesson 7.2: Human-in-the-Loop

*The Ultimate Safety Net*

## Introduction

No matter how smart an agent is, there are things it should **not** do (e.g., admitting a legal mistake) or **cannot** do (e.g., empathizing with a deeply frustrated customer). **Human-in-the-Loop** (HITL) is a pattern where the AI stops and waits for a human to approve an action or take over the conversation.

---

## 1. When to Escalate to a Human

Good agents recognize their own limits. Typical reasons for escalation include:

- **Explicit Request**: "I want to speak to a manager."
- **Sensitive Topics**: Complaints about safety, discrimination, or legal threats.
- **Complex Logic**: Situations that fall outside the agent's tools or business rules.

---

## 🛠️ In Our Project: The Escalation Tool

We give our agents the power to call for help using a specific tool.

**In our code (`backend/src/tools.py`):**

```python
@tool
def escalate_to_human(customer_id: str, reason: str, priority: str = "normal") -> dict:
    """Escalate a conversation to a human support agent. Use this for complex complaints..."""
    # Logic to create a support ticket in our 'T000' system
    ...
```

When this tool is called, the AI's job is done—the "State" can now be handed over to a human dashboard where a real person sees the full conversation history.

---

## 2. HITL: Interrupt and Approve

In more advanced systems, LangGraph allows you to **Interrupt** the graph.

1. Agent plans a tool call: `db_process_refund(amount=1000)`.
2. LangGraph pauses execution.
3. An admin clicks "Approve" in a dashboard.
4. LangGraph resumes and calls the tool.

This ensures that the AI never spends large amounts of money without a "Human Eye" on the transaction.

---

## Summary

Human-in-the-Loop is not a failure of AI—it is a feature of a well-designed system. By building ways for your agent to ask for help, you create a service that is both helpful and safe.

> [!CAUTION]
> **Don't Over-Escalate**: If your agent escalates every single question, it's not saving you any work. Balance the autonomy of the agent with the safety of human oversight.
