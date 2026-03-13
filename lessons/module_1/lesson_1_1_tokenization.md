# Lesson 1.1: Tokenization and Probability

*How Models See our Catalog*

## Introduction

Before an LLM can reason about our "SoundMax headphones," it first has to "see" the text. Models don't read words like humans do; they read **Tokens**.

---

## 1. What is a Token?

A token is a chunk of text. It can be a whole word, a part of a word (like a prefix or suffix), or even just a single character or punctuation mark.

**Example**:
> "ProBook Laptop"
Might be broken into tokens like: `[Pro] [Book] [ Laptop]`

### Why does this matter?

- **Efficiency**: Splitting words into chunks allows the model to understand related words (e.g., `run`, `running`, `runner` all share the `run` token).
- **Limits**: Models have a "Context Window" (which we'll cover in Lesson 1.3) that is measured in tokens, not words.

---

## 2. Probability: The "Next Token" Prediction

Modern AI models are essentially super-advanced "autocomplete" engines. They predicting the **most likely next token** based on the prompt.

### 🛠️ In Our Project: The Product Description

When our **Product Agent** generates a description for `P001` (ProBook Laptop), it's playing a game of probability:

**Prompt**: *"The ProBook 15 is a..."*

- Token A: `powerful` (Probability: 45%)
- Token B: `laptop` (Probability: 30%)
- Token C: `banana` (Probability: 0.001%)

The model chooses the next token based on its training. If it chooses `powerful`, it then calculates the probability for the *next* token after that.

---

## 3. The "Attention" Mechanism

How does the model know it's a "laptop" and not a "shoe"? It uses **Attention**.
It looks back at the earlier tokens in the sentence (`ProBook`, `Laptop`) to decide the context for the current token. In our project, if the user mentions "refund," the model "attends" to that word to shift its reasoning toward the **Order Agent** logic.

---

## Summary

LLMs are probabilistic engines that process text as tokens. By predicting the most likely next token, they create responses that feel intelligent.

> [!TIP]
> **Token Rule of Thumb**: For English text, 1,000 tokens is roughly equivalent to 750 words.
