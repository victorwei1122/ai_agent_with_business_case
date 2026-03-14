# Lesson 4.3: Tools and Toolkits

*Giving the Agent Specialized Skills*

## Introduction

In LangChain, a **Tool** is not just a function—it's a standardized interface that allows any LLM to understand how to interact with your code. When you group multiple tools together, you create a **Toolkit**.

---

## 1. Defining a Tool

LangChain provides the `@tool` decorator, which automatically turns a Python function into a tool the AI can use.

The most important part of a tool is its **Type Hints** and **Docstrings**. LangChain uses these to generate the JSON schema that is sent to the LLM.

**In our code (`backend/src/agents/order_agent.py`):**

```python
@tool
def db_lookup_order(order_id: str) -> Dict[str, Any]:
    """Look up an order by its ID. Returns status and tracking..."""
```

- **The Name**: `db_lookup_order`
- **The Type Hint**: `order_id: str` (The AI knows it must provide a string)
- **The Docstring**: Tells the AI *when* to use this tool.

---

## 2. Structured Tools

Sometimes a tool needs complex inputs (like an object with many fields). LangChain supports this via Pydantic models.

**Example**: In our [order_agent.py](../../backend/src/agents/order_agent.py), we defined a schema for creating support tickets:

```python
from pydantic import BaseModel, Field

class TicketSchema(BaseModel):
    order_id: str = Field(description="The order ID this ticket is related to")
    subject: str = Field(description="Short summary of the issue")
    priority: str = Field(description="Priority level: 'low', 'normal', 'high', 'urgent'")
    description: str = Field(description="Detailed explanation of the problem")

@tool(args_schema=TicketSchema)
def db_create_support_ticket(order_id: str, subject: str, priority: str, description: str):
    """Create a new support ticket for a customer issue."""
    ...
```

---

## 🛠️ In Our Project: The `order_tools` List

We group our related tools into a list. This is essentially our "Order Toolkit."

```python
order_tools = [db_lookup_order, db_process_refund, db_get_sales_analytics]
```

When we call `.bind_tools(order_tools)`, the LLM is given the instructions for all three skills at once. It chooses between them based on the descriptions we wrote.

---

## 3. Toolkits

LangChain provides pre-built **Toolkits** for common tasks. Instead of defining tools manually, you can ingest a whole suite of capabilities at once.

### A. SQLDatabaseToolkit

This is incredibly powerful for internal business tools. It allows an agent to:

1. List tables in a database.
2. Inspect the schema of specific tables.
3. Execute SQL queries and receive the results.
4. Check its own SQL syntax for errors.

**Implementation Example** (see [research_agent.py](../../backend/src/agents/research_agent.py)):

```python
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from src.db.database import SQLALCHEMY_DATABASE_URL

# Connect using the project's unified database URL (SQLite or Postgres)
db = SQLDatabase.from_uri(SQLALCHEMY_DATABASE_URL)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# This adds 4 tools: query, schema, list_tables, and query_checker
tools = toolkit.get_tools()
```

### B. Search Tools (e.g. Tavily)

To give your agent access to real-time information (like current stock market prices or news), you can use a search tool. **Tavily** is a search engine optimized specifically for AI agents.

```python
from langchain_community.tools.tavily_search import TavilySearchResults

# k=3 returns the top 3 results
search_tool = TavilySearchResults(k=3)
```

---

---

## 🚀 Hands-on: See it in Action

We have integrated these toolkits into a specialized **Research Agent** within our orchestrator ([graph.py](../../backend/src/graph.py)).

### Try it in the Chat

1. **SQL Toolkit**: Ask the bot: *"What are all the table names in our system?"*
    - The **Supervisor** will route to the **Research Agent**.
    - The **Research Agent** will use the `SQLDatabaseToolkit` to list the tables.
2. **Search Tool**: Ask the bot: *"What are some popular AI agent trends in 2024?"*
    - The agent will use the `TavilySearchResults` tool to browse the web!

### Why this matters

By using **Toolkits**, we didn't have to write custom code to explore the database. We simply gave the AI a "professional kit" and let it figure out how to use the specific tools inside it.

---

## Summary

Tools are how we extend an LLM's knowledge and actions. By standardizing these skills into tools, we can reuse them across different agents and projects.

> [!IMPORTANT]
> **Safety First**: Tools are powerful. Always ensure your tools have "Guardrails"—like checking permissions or limiting results—before exposing them to an AI.
