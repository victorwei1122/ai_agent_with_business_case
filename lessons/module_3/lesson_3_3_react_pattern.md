# Lesson 3.3: ReAct Pattern

*The Brains and the Brawn*

## Introduction

How does an agent actually decide when to use a tool versus when to just talk? The most popular framework for this is called **ReAct** (Reasoning and Acting). It is the backbone of almost every modern AI agent.

---

## 1. What is ReAct?

ReAct is a prompting strategy where the model is trained to interleave its **thought process** (Reasoning) with **tool execution** (Acting).

A ReAct turn looks like this:

1. **Thought**: "I need to find the user's order to see the status."
2. **Action**: `db_lookup_order(order_id="123")`
3. **Observation**: "Order 123 is delivered."
4. **Thought**: "The order is already delivered, so I can't cancel it."
5. **Final Answer**: "I'm sorry, I cannot cancel this order because it has already been delivered."

---

## 2. Why it Matters

Without the "Reasoning" step, agents often make "blind" tool calls. They might try to process a refund without checking if the order exists first. ReAct forces the model to justify its next move.

---

## 🛠️ In Our Project: The System Prompt

In our project, we "pre-load" our agents with the ReAct mindset using the **System Message**.

**In our project's global prompt (`backend/src/prompts.py`):**

```text
Analyze the user's request carefully. 
If you need data, call the appropriate tool. 
Look at the results of your tool calls to formulate your next response.
```

By instructing the model to *analyze* before *responding*, we are implementing a lightweight version of ReAct.

---

## 3. The Supervisor as a Manager

Our **Supervisor Agent** (in `backend/src/graph.py`) also uses a form of ReAct. It takes the "Observation" of what the user said, "Reasons" about which agent is best, and then "Acts" by routing the thread.

This multi-agent teamwork is just a scaled-up version of the ReAct pattern!

---

## Summary

ReAct is the "inner monologue" of an agent. It combines the logical planning we learned in Module 2 (Chain-of-Thought) with the practical execution we learned in Lesson 3.2 (Tool Calling).

---

## What's Next?

Now that we understand how agents think and act on their own, we need a framework to organize these complex patterns. In **Module 4**, we will explore **LangChain**—the library that makes all of this happen programmatically.

> [!NOTE]
> ReAct was first introduced in a paper by Google Research and Princeton. It proved that models that "talk to themselves" are much better at interacting with APIs than models that just output code directly.
