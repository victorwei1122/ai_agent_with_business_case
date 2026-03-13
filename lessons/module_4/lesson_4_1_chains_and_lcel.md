# Lesson 4.1: Chains & LCEL

*The "Pipe" Operator of AI*

## Introduction

In Module 3, we saw how to build a ReAct loop manually using `while` loops and `if` statements. While that works, it becomes messy as systems grow. **LangChain** was built to solve this using **LCEL** (LangChain Expression Language).

---

## 1. What are Chains?

A "Chain" is a sequence of calls—to an LLM, a tool, or a data transformation.

Instead of writing:

```python
prompt = create_prompt(input)
response = llm.invoke(prompt)
result = parse_response(response)
```

LCEL allows you to "pipe" them together like a Unix terminal:

```python
chain = prompt | llm | parser
result = chain.invoke(input)
```

---

## 2. Why use LCEL?

- **Streaming**: It supports streaming results by default.
- **Async**: It handles asynchronous calls natively.
- **Parallelism**: You can run multiple chains at once.

---

## 🛠️ In Our Project: Tool Binding as a Chain

Even though we have a custom loop in `order_agent.py`, we use the beginning of a chain to set up our model.

**In our code (`backend/src/agents/order_agent.py`):**

```python
# This is a mini-chain!
# It combines the model with the tool definitions.
llm = get_llm(temperature=0).bind_tools(order_tools)
```

By using `.bind_tools()`, we are telling LangChain: "Every time I call this LLM, I want it to be aware of these specific tools."

---

## 3. The Power of "Composition"

Imagine you want to translate a user's question before the agent answers it. With LCEL, it's easy:

```python
translation_chain = translation_prompt | llm | StrOutputParser()
full_agent_chain = translation_chain | agent_chain
```

---

## Summary

Chains and LCEL are the "glue" that holds AI applications together. They allow us to combine models, prompts, and tools into a single, predictable unit of work.

> [!TIP]
> Think of LCEL as **LEGO blocks** for AI. Each block has a specific input and output, and you can snap them together to build complex machines.
