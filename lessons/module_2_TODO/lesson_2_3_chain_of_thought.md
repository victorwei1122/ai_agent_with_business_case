# Lesson 2.3: Chain-of-Thought (CoT)

*The Power of Thinking Out Loud*

## Introduction

Early AI models were like a student who shouts an answer instantly without showing their work. While fast, they were often wrong on complex tasks. **Chain-of-Thought (CoT)** is a technique that forces the AI to "think step-by-step" before arriving at a final answer.

---

## 1. Why CoT Works

LLMs predict the next token. If a model tries to answer a math problem in one token, the probability of it being right is low. But if the model has to write out 5 sentences of reasoning first, each sentinel of reasoning guides it closer to the correct conclusion.

In the world of agents, CoT is required for **Tool Selection**.

---

## 2. Standard CoT vs. Zero-shot CoT

- **Zero-shot CoT**: You simply add the phrase *"Let's think step by step"* to the end of your prompt. It's surprisingly effective for improving logic.
- **Structured CoT**: You instruct the model to always provide a "Reasoning," "Action," and "Observation" (this is the ReAct pattern, which we cover in Module 3).

---

## 🛠️ In Our Project: Multi-Agent Reasoning

When our **Supervisor** receives a complex request, it has to use chain-of-thought (mentally) to decide where to go.

**User Question**: *"Is the SoundMax headphones your best seller?"*

**The "Invisible" Chain of Thought**:

1. The user is asking about a specific product (`SoundMax`).
2. They are asking about its popularity/sales status (`best seller`).
3. The **Product Agent** knows features, but the **Order Agent** has the `db_get_sales_analytics` tool.
4. **Conclusion**: I should route this to the `order_agent`.

---

## 3. Designing for Reasoning

When you write a System Message for a complex agent, include a section about reasoning:

```text
Before choosing a tool, explain your reasoning in one sentence. 
Analyze the user's intent and determine which data source is required.
```

---

## Summary

Chain-of-Thought reduces errors by slowing the model down and forcing it to create a logical path to the answer. In agentic systems, this is the difference between a random guess and a precise action.

> [!NOTE]
> DeepMind research found that for complex reasoning tasks, models with CoT active performed up to **300% better** than those without it.
