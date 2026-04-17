# Deep Dive: Knowledge Graph Internals (The Property Graph Model)

When designing advanced AI Agent architectures, understanding how data is structured *behind the scenes* of a Knowledge Graph (like Neo4j) is a massive advantage in system design interviews.

Unlike relational databases (SQL) which use rigid tables and columns, modern enterprise graph databases use the **Property Graph Model**.

## The Three Pillars of a Property Graph

A Property Graph dataset is built entirely out of three concepts:
1. **Nodes:** The entities themselves (e.g., a Client, a Company, a Document).
2. **Edges (Relationships):** The directional, named lines connecting nodes (e.g., `OWNS_STOCK_IN`, `GOVERNS`).
3. **Properties:** Key-value pairs of data that can be attached to *both* Nodes and Edges.

## Where do the Vectors/Embeddings go?

**Yes, modern graph databases natively store vector embeddings!** 

Because a Node can hold any "Property" (just like a JSON object), the massive array of floats representing the embedding (e.g., the output from OpenAI's `text-embedding-3-small` model) is simply stored as an array property inside the node alongside its normal text data. 

In Neo4j, you then command the database to build a "Vector Search Index" explicitly on that specific property field.

---

## What it looks like "Under the Hood"

If you were to peek behind the curtain of the database, a Node does not look like a spreadsheet row. It is stored almost exactly like a JSON object.

### The Node (Containing the Embedding)

```json
// Node 1042: A Public Company
{
  "_id": 1042,
  "labels": ["Company", "Tech_Sector"],
  "properties": {
    "name": "Apple Inc.",
    "ticker": "AAPL",
    "market_cap": "3T",
    "description": "Apple designs consumer electronics and software.",
    
    // THIS is where your vector embedding lives!
    "description_embedding": [0.145, -0.092, 0.881, 0.553, ...1536 floats...] 
  }
}
```

### The Edge (Containing its own Properties)

Edges are incredibly powerful because they aren't just invisible links—they hold data too.

```json
// Edge 9934: The relationship connecting a Customer to a Company
{
  "_id": 9934,
  "type": "OWNS_STOCK_IN",
  "from_node_id": 551,  // Points to Customer: John Smith
  "to_node_id": 1042,   // Points to Company: Apple Inc.
  "properties": {
    "shares_owned": 500,
    "purchase_date": "2024-01-15",
    "account_type": "TFSA"
  }
}
```

---

## The Execution: Hybrid GraphRAG

During an interview, explaining how a search executes within this structure proves you understand the data layer. Here is the 1-2 punch of **Hybrid Graph Search**:

**The Prompt:** *"Does John own stock in the company that makes iPhones?"*

**Step 1 (The Vector Jump):** 
The graph database takes the word `"iPhones"`, converts it to a vector, and compares it against all the `description_embedding` properties in the database using cosine similarity. It "lands" on the `Apple Inc.` node computationally.

**Step 2 (The Graph Traversal):** 
Once the database has landed on the Apple node, it completely stops doing vector math (which is expensive, fuzzy, and prone to hallucinations). Instead, it rapidly traverses the graph by following the hard-coded `OWNS_STOCK_IN` edge backward to deterministically find the "John Smith" node.

> [!TIP]
> **The Interview Mic-Drop:** "By storing vector embeddings *inside* the nodes as a property, we achieve the best of both worlds: the fuzzy-matching, conceptual superpowers of a Vector DB, combined with the 100% accurate, deterministic logical routing of a Graph DB."
