# Lesson 4.2: Core Components

*Models, Prompts, and Parsers*

## Introduction

LangChain organizes the chaos of AI development by providing standardized objects for every part of the stack.

---

## 1. Chat Models

A **Chat Model** is an abstraction over different AI providers (Gemini, OpenAI, Ollama). It allows you to write code once and switch models easily.

**In our code (`backend/src/agents/llm_utils.py`):**

```python
# Our 'get_llm' function can return a Google or Ollama model
if provider == "ollama":
    llm = ChatOllama(...)
else:
    llm = ChatGoogleGenerativeAI(...)
```

Because both `ChatOllama` and `ChatGoogleGenerativeAI` follow the same LangChain standard, the rest of our code doesn't care which one we use.

---

## 2. Prompt Templates

Instead of using f-strings to build prompts, LangChain uses **Prompt Templates**. These allow you to define placeholders that are filled at runtime.

**In our agents:**
We use `SystemMessage` and `HumanMessage` objects. These are "pre-parsed" versions of a template that the LLM understands as different roles.

---

## 3. Output Parsers

LLMs return text, but programs often need data. **Output Parsers** take that raw text and turn it into something useful, like a Python list or a JSON object.

We saw this in **Module 2: Lesson 2.4**. In LangChain, we often use the `PydanticOutputParser` to guarantee that the agent's response matches a specific structure.

---

## 🛠️ In Our Project: The `clean_tool_args` logic

While we wrote a custom function to clean up tool arguments, LangChain has built-in tools for this. However, by writing our own, we learned how "under the hood" parsers work!

Every time you see `json.loads()` or `json.dumps()` in our code, we are essentially performing **Output Parsing**.

---

## Summary

By using standard components, we ensure that our agent is:

- **Portable**: Can move from one model provider to another.
- **Reliable**: Prompts and outputs are consistent.
- **Maintainable**: The code is organized into logical pieces.

> [!NOTE]
> Even if you use a high-level framework like LangGraph (Module 5), you are still using these same core components underneath.
