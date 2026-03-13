# Lesson 1.2: Temperature & Top-P

*Balancing Accuracy and Creativity*

## Introduction

Not all responses should be creative. If you ask about an order status, you want a factual, deterministic answer. If you ask for a product recommendation, you might want something more conversational. This balance is controlled by **Temperature**.

---

## 1. Temperature: The Randomness Dial

Temperature controls how much risk the model takes when picking the next token.

- **Temperature 0 (Deterministic)**: The "Greedy" mode. The model *only* ever picks the single most likely token.
  - *Result*: 100% predictable. If you ask the same question twice, you get the exact same answer. Perfect for data, math, and code.
- **Low Temperature (0.1 - 0.3)**: Stable but slightly varied.
  - *Result*: Focused and predictable, but with enough "wiggle room" to not sound like a robot repeating a script.
- **High Temperature (0.7 - 1.0+)**: Creative and diverse.
  - *Result*: Human-like and varied, but carries a higher risk of losing the plot (hallucination).

---

## 2. Top-P (Nucleus Sampling)

Top-P is another way to control diversity. It tells the model to only look at the top "X" percent of probable tokens.

- *Example*: If Top-P is 0.1, the model only looks at the tokens that make up the top 10% of probability mass.

---

## 🛠️ In Our Project: Fact vs. Flavor

In our e-commerce business case, we need to balance these settings depending on the agent:

### Case A: The Order Agent (Temperature 0)

When checking an order status like `1001`, accuracy is everything. We use `0` temperature to ensure the agent doesn't "hallucinate" a delivery date.

**In our code (`backend/src/agents/order_agent.py`):**

```python
# Explicitly set temperature=0 for deterministic data fetching
llm = get_llm(temperature=0).bind_tools(order_tools)
```

### Case B: The Product Agent (Temperature 0.7)

When describing the `SoundMax Headphones`, we want some flavor. We use `0.7` temperature to make the sales pitch feel fresh and varied.

**In our code (`backend/src/agents/product_agent.py`):**

```python
# Set temperature=0.7 for creative and engaging recommendations
llm = get_llm(temperature=0.7).bind_tools(product_tools)
```

---

## 4. The Top-P Alternative

Temperature is the most important setting for controlling an agent's "personality." Use low temperature for data-heavy tasks and higher temperature for creative tasks.

> [!WARNING]
> **Hallucination Risk**: As temperature increases, the model is more likely to pick "random" tokens that aren't grounded in reality. Never use high temperature for code or math!
