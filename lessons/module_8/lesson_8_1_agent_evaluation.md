# Lesson 8.1: Agent Evaluation

*How Do You Know if It Works?*

## Introduction

You can't just "feel" that an agent is working. For a business, you need proof. **Agent Evaluation** (Eval) is the process of measuring accuracy, safety, and helpfulness using data.

---

## 1. The Challenges of AI Testing

Traditional software has "Unit Tests"—if `1 + 1` doesn't equal `2`, the test fails. But AI is probabilistic. It might answer the same question in three different (but correct) ways.

---

## 2. Types of Evaluation

### A. LLM-as-a-Judge

You use a "stronger" model (like Gemini Ultra or GPT-4o) to grade the response of your "smaller" agent.

- **Criteria**: "Did the agent mention the SoundMax headphones?", "Was the tone polite?", "Was the answer factually correct?"

### B. Gold Sets (Ground Truth)

You create a list of 100 questions and the *perfect* answers. Every time you change your code, you run all 100 questions and see how close the agent gets to the perfect answers.

---

## 🛠️ In Our Project: Testing the Supervisor

In our project's **Verification Plan**, we defined specific scenarios to test.

**Example Test case**:

- **Query**: "What is your best seller?"
- **Success Criteria**:
    1. The Supervisor must route the message to the **Order Agent**.
    2. The final answer must mention **"SoundMax"**.

If the Supervisor sends this query to the "General Agent," our test has failed, even if the General Agent gives a polite response.

---

## 3. Tool Accuracy

For agents, you must also test **Tool Selection**. If a user asks for a refund and the agent calls the "Product Search" tool, the evaluation score is 0.

---

## Summary

Evaluation is what allows you to ship AI with confidence. By creating a rigorous testing process, you ensure that your agent solves business problems without creating new ones.

> [!TIP]
> **Start Small**: You don't need fancy software to start. A simple CSV file with 10 questions and 10 "Correct" agents is a great beginning for any project.
