# Lesson 2.2: Zero-shot, One-shot, and Few-shot Learning

*Teaching via Examples*

## Introduction

How much information does an AI need to solve a task? Depending on the complexity, you might give it just a command, one example, or many examples. These techniques are called **Zero-shot**, **One-shot**, and **Few-shot** learning.

---

## 1. Zero-shot Learning

Zero-shot means you give the AI a task with no examples of how to do it. You rely entirely on the model's pre-existing knowledge.

- **Example**: *"Classify this review as positive or negative: 'I love this laptop!'"*
- **Pros**: Very simple and fast.
- **Cons**: High risk of the AI formatting the answer incorrectly or misunderstanding a complex rule.

---

## 2. One-shot Learning

One-shot means you provide exactly one example of a successful input and output before asking the AI to perform the task.

- **Example**:
  > *"Classify this review: 'The screen is dim.' -> Negative.
  > Now classify this: 'The battery lasts all day.' -> "*
- **Pros**: Dramatically improves accuracy and formatting.

---

## 3. Few-shot Learning

Few-shot means you provide a small set (usually 3-5) of examples. This is the "gold standard" for ensuring an agent behaves exactly how you want.

- **Pros**: Excellent for handling edge cases and specialized formatting (like JSON).

---

## 🛠️ Case Study: Our Supervisor Agent

In `backend/src/graph.py`, our **Supervisor** uses a Zero-shot approach to route messages. It has instructions, but no examples.

### current (Zero-shot)

```text
Respond ONLY with a JSON object in this format: {"route": "<agent_name>"}
```

### Improved (Few-shot)

If our supervisor starts making mistakes (e.g., routing "I want a refund" to the Product Agent), we can add Few-shot examples to its prompt:

```text
User: "Where is my package?"
{"route": "order_agent"}

User: "I need a gaming laptop."
{"route": "product_agent"}

User: "Hello!"
{"route": "general"}
```

By seeing these patterns, the model understands the logic behind the routing much better than it would from instructions alone.

---

## Summary

When building agents, always start with Zero-shot. If the agent fails or gives inconsistent results, move to Few-shot by adding 3-5 clear examples to your prompt.

> [!IMPORTANT]
> **Diversity is Key**: When using Few-shot, provide examples that cover different situations. If all your examples are about refunds, the agent might start thinking *everything* is a refund!
