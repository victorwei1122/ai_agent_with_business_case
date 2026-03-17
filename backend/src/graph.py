from typing import Dict, TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from src.agents.llm_utils import get_llm, get_text_content
from src.agents.order_agent import invoke_order_agent
from src.agents.product_agent import invoke_product_agent
from src.agents.research_agent import invoke_research_agent
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the state for the LangGraph orchestrator
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next_agent: str
    thoughts: Annotated[Sequence[str], operator.add]

def supervisor_node(state: AgentState) -> Dict:
    """
    The Supervisor LLM decides which specialized agent should handle the user's query,
    or if it has enough information to provide a final synthesized answer.
    """
    messages = state["messages"]
    
    # We use a structured output prompt to force the LLM to pick a route OR finish
    system_prompt = """You are the **Team Lead Supervisor** for ShopSmart Inc. 
Your goal is to coordinate specialized agents to provide the best possible answer to the user.

### YOUR CAPABILITIES:
1. **ORCHESTRATION**: Routing to specialized agents to gather data.
2. **SYNTHESIS**: Reviewing findings from all agents and writing the final response.

### SPECIALIZED AGENTS:
- "order_agent": For order status, tracking, refunds, or sales analytics.
- "product_agent": For searching/recommending products from the catalog.
- "research_agent": For customer reviews (sentiment), DB schema, or web research.

### RULES:
- If the user's question requires multiple angles (e.g., "Recommend a popular laptop with good reviews"), call agents sequentially.
- Once you have all the data needed in the conversation history, choose "FINISH" and write the final response.
- NEVER name the tools or internal agent names in the final response.

Respond ONLY with a JSON object:
{"route": "order_agent" | "product_agent" | "research_agent" | "FINISH", "reasoning": "A short sentence explaining why you chose this path"}
"""
    
    # Set temperature=0 for deterministic routing
    llm = get_llm(temperature=0).with_config({"run_name": "Supervisor"})
    
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        *messages
    ])
    
    thoughts = []
    try:
        content = get_text_content(response)
        # Clean up the response in case it has markdown block formatting
        content = content.replace("```json", "").replace("```", "").strip()
        decision = json.loads(content)
        route = decision.get("route", "FINISH")
        reasoning = decision.get("reasoning", "")
        if reasoning:
            thoughts.append(f"[Supervisor] {reasoning}")
        # Validate route
        if route not in ["order_agent", "product_agent", "research_agent", "FINISH"]:
            route = "FINISH"
    except Exception as e:
        logger.error(f"Failed to parse supervisor JSON: {response.content}. Error: {e}")
        route = "FINISH"
        
    logger.info(f"Supervisor decided to route to: {route}")
    return {"next_agent": route, "thoughts": thoughts}

def order_agent_node(state: AgentState) -> Dict:
    """Invokes the Order Agent via its LangChain function."""
    user_input = state["messages"][-1].content
    result = invoke_order_agent(user_input)
    # Prefix the response so we know which sub-agent handled it in the UI (optional, but good for demo)
    return {
        "messages": [AIMessage(content=f"[From Order Agent] {result['response']}")],
        "thoughts": [f"[Order Agent] {t}" for t in result.get("thoughts", [])]
    }

def product_agent_node(state: AgentState) -> Dict:
    """Invokes the Product Agent via its LangChain function."""
    user_input = state["messages"][-1].content
    result = invoke_product_agent(user_input)
    return {
        "messages": [AIMessage(content=f"[From Product Agent] {result['response']}")],
        "thoughts": [f"[Product Agent] {t}" for t in result.get("thoughts", [])]
    }

def research_agent_node(state: AgentState) -> Dict:
    """Invokes the Research Agent via its toolkit-powered function."""
    user_input = state["messages"][-1].content
    result = invoke_research_agent(user_input)
    return {
        "messages": [AIMessage(content=f"[From Research Agent] {result['response']}")],
        "thoughts": [f"[Research Agent] {t}" for t in result.get("thoughts", [])]
    }

def final_answer_node(state: AgentState) -> Dict:
    """
    The Supervisor synthesizes all information gathered so far into a final response.
    """
    messages = state["messages"]
    llm = get_llm(temperature=0.7)
    
    system_prompt = (
        "You are **SmartBot**, the friendly and professional final responder for ShopSmart. "
        "Review the conversation history, which includes data gathered by specialized agents. "
        "Synthesize all findings into a single, cohesive, and helpful response for the user. "
        "\n\n### GROUNDING GUARDRAIL:"
        "\n- If you mention products that were NOT found in the local catalog (provided by product_agent), "
        "you MUST explicitly state that those specific items are not currently in our store's inventory "
        "but are recommended based on general knowledge or the internet."
        "\n- ALWAYS prioritize the products that ARE in our catalog."
        "\n- DO NOT use raw data or list previous agent names."
    )
    
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        *messages
    ])
    
    return {"messages": [AIMessage(content=get_text_content(response))]}

# Define the edge routing logic
def route_to_agent(state: AgentState) -> str:
    return state.get("next_agent", "FINISH")

# Build the LangGraph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("order_agent", order_agent_node)
workflow.add_node("product_agent", product_agent_node)
workflow.add_node("research_agent", research_agent_node)
workflow.add_node("final_answer", final_answer_node)

# Set the entry point
workflow.set_entry_point("supervisor")

# Add conditional edges from supervisor
workflow.add_conditional_edges(
    "supervisor",
    route_to_agent,
    {
        "order_agent": "order_agent",
        "product_agent": "product_agent",
        "research_agent": "research_agent",
        "FINISH": "final_answer"
    }
)

# Agents return to supervisor for next steps
workflow.add_edge("order_agent", "supervisor")
workflow.add_edge("product_agent", "supervisor")
workflow.add_edge("research_agent", "supervisor")
workflow.add_edge("final_answer", END)

# Add persistence
memory = MemorySaver()

# Compile!
app_graph = workflow.compile(checkpointer=memory)
