# Lesson 0.1: Defining AI

*From Code to Intelligence*

## Introduction

Before we build agents, we need to understand the "Brain" that powers them: **Artificial Intelligence (AI)**. But what actually *is* it?

In simple terms, AI is a field of computer science that builds systems capable of performing tasks that usually require human intelligence—like understanding language, recognizing faces, or making decisions.

---

## 1. The Three Eras of AI

To understand where we are, we have to see where we came from.

### Era 1: Symbolic AI (The "If-Then" Era)

Early AI was based on strict rules defined by humans.

- **How it worked**: Developers wrote thousands of `if-then` statements.
- **Limitation**: It couldn't handle "gray areas." If a situation wasn't explicitly coded, the system failed.
- **Example**: A chess engine that only knows a fixed set of moves.

### Era 2: Traditional Machine Learning (The "Pattern" Era)

Instead of rules, we gave the computer **data**.

- **How it worked**: We showed the computer 10,000 pictures of cats. It learned the patterns (ears, whiskers) itself.
- **Limitation**: It required massive amounts of "labeled" data and was still narrow (a cat-detector couldn't write a poem).

### Era 3: Generative AI (The "Creative" Era) — *Where we are now*

This is the era of **Large Language Models (LLMs)** like Gemini and GPT.

- **How it works**: They don't just find patterns; they understand the *probabilities* of information. They have read almost everything on the internet and can "generate" new content based on that vast knowledge.
- **The Breakthrough**: They can reason, summarize, and solve problems they weren't specifically trained for.

---

## 2. Why Generative AI is Different

Unlike previous AI, Generative AI is **Universal**.
The same model that helps you write a Python script can also write a legal contract or explain a joke. This "General Purpose" nature is what makes it possible to build **Agents**.

## 3. Key Vocabulary

- **Model**: The "Brain" file that has been trained on data.
- **Inference**: The act of asking the model a question and getting an answer.
- **Prompt**: The instruction you give to the model.

---

## 🛠️ In Our Project: The Brain

In this course's repository, we use **Gemini Flash** as our reasoning engine. You can see this configured in `backend/config.yml`:

```yaml
llm_provider: "gemini"
# This tells our agents to use Google's Gemini model 
# for all their internal reasoning and responses.
```

---

## Summary

AI has evolved from strict rules to flexible, creative reasoning. Today's LLMs are the first step toward systems that don't just follow instructions, but actually understand the goal.

> [!TIP]
> **Think of it this way**: Old software followed a recipe. Modern AI is like a chef who understands *why* certain ingredients go together and can create a new dish on the fly.
