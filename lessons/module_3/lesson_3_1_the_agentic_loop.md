# Lesson 3.1: The Agentic Loop

*Moving from Static Answers to Dynamic Conversations*

## Introduction

The biggest difference between a "Chatbot" and an "Agent" is the **Agentic Loop**. While a chatbot gives one final answer based on its training, an agent enters a cycle of thinking and acting until the job is done.

---

## 1. The Core Loop: Plan -> Act -> Observe

Almost every autonomous agent follows this simple cycle:

1. **Plan**: The AI analyzes the user's request and decides what to do next (e.g., "I need to look up order 1001").
2. **Act**: The AI performs an action, such as calling a tool or searching a database.
3. **Observe**: The AI looks at the *result* of that action (e.g., "The database says order 1001 is SHIPPED").
4. **Repeat**: Based on the observation, the AI plans the next step or gives a final answer.

---

## 🛠️ In Our Project: The `for` Loop

In our code, we implement this loop manually to ensure the agent has multiple "turns" to solve a problem.

**In our code (`backend/src/agents/order_agent.py`):**

```python
# The loop allows the agent up to 5 "turns" to solve the query
for i in range(5):
    response = llm.invoke(messages)
    messages.append(response)
    
    # If the response contains a tool call (Action)
    if response.tool_calls:
        # 1. Plan: The LLM decided to use a tool
        # 2. Act: We execute the tool
        # 3. Observe: We append the result back to messages
        ...
        continue # Loop back to 'Plan' the next move
        
    # If no more tools are needed, we return the final answer
    return get_text_content(response)
```

### Understanding the Loop

It's common to mistake this `for` loop for "retrying" the same question. Here is what is actually happening:

1. **Sequence, not Competition**: This is a **sequence of turns**, not 5 separate attempts to pick the "best" answer. Each turn builds on the last (e.g., Turn 1: Lookup Order -> Turn 2: Process Refund -> Turn 3: Final Answer).
2. **Building Context (Memory)**: Inside the loop, we use `messages.append(response)`. This means the agent **remembers** what happened in the previous turn. If a tool returns an error, the agent sees that in the next turn and can correct itself.
3. **The Safety Rail**: We set `range(5)` as a maximum limit. Most requests only take 1–2 turns. If an agent gets stuck in an "infinite loop" (trying the same failing action repeatedly), this prevents it from wasting time and API costs.

---

## 2. Autonomy through Observation

The most "agentic" part of this loop is the **Observe** phase. Because the agent sees the result of its tools, it can correct itself.

- **Scenario**: User asks for "best selling product."
- **Turn 1**: Agent calls `db_get_sales_analytics(product_name="best")`.
- **Turn 1 Observation**: Tool returns 0 results (maybe "best" isn't a product name).
- **Turn 2 (Correction)**: Agent realizes its mistake and calls `db_get_sales_analytics()` (no arguments) to get the general top list.
- **Turn 2 Observation**: Tool returns the Top 5 list.
- **Final Answer**: Agent presents the list to the user.

---

## Summary

Building an agent isn't just about a better prompt; it's about building a **system** that allows the AI to iterate, observe results, and refine its approach.

> [!TIP]
> The Agentic Loop is what allows an AI to handle ambiguity. If the user's request is unclear, the agent can use the first turn of the loop to ask for clarification or check multiple data sources.
