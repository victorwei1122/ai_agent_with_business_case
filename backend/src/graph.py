from typing import Dict, TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from src.agents.llm_utils import get_llm, get_text_content
from src.agents.order_agent import invoke_order_agent
from src.agents.product_agent import invoke_product_agent
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the state for the LangGraph orchestrator
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next_agent: str

def supervisor_node(state: AgentState) -> Dict:
    """
    The Supervisor LLM decides which specialized agent should handle the user's query.
    """
    messages = state["messages"]
    user_input = messages[-1].content
    
    # We use a structured output prompt to force the LLM to pick a route
    system_prompt = """You are a supervisor routing customer queries for an e-commerce store.
Based on the user's message, decide which agent should handle it.
Respond ONLY with a JSON object in this exact format: {"route": "<agent_name>"}

Available routes:
- "order_agent": For questions about order status, tracking, refunds, or sales/popularity statistics (e.g., "how many were sold?", "what is the best seller?").
- "product_agent": For questions about finding, recommending, or buying products based on their features and categories.
- "general": For greetings or questions that don't fit the above.
"""
    
    # Set temperature=0 for deterministic routing
    llm = get_llm(temperature=0).with_config({"run_name": "Supervisor"})
    
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        # Include previous messages for context
        *messages
    ])
    
    try:
        content = get_text_content(response)
            
        # Clean up the response in case it has markdown block formatting
        content = content.replace("```json", "").replace("```", "").strip()
        decision = json.loads(content)
        route = decision.get("route", "general")
        # Validate route
        if route not in ["order_agent", "product_agent", "general"]:
            route = "general"
    except Exception as e:
        logger.error(f"Failed to parse supervisor JSON: {response.content}. Error: {e}")
        route = "general"
        
    logger.info(f"Supervisor decided to route to: {route}")
    return {"next_agent": route}

def order_agent_node(state: AgentState) -> Dict:
    """Invokes the Order Agent via its LangChain function."""
    user_input = state["messages"][-1].content
    response_text = invoke_order_agent(user_input)
    # Prefix the response so we know which sub-agent handled it in the UI (optional, but good for demo)
    return {"messages": [AIMessage(content=f"[From Order Agent] {response_text}")]}

def product_agent_node(state: AgentState) -> Dict:
    """Invokes the Product Agent via its LangChain function."""
    user_input = state["messages"][-1].content
    response_text = invoke_product_agent(user_input)
    return {"messages": [AIMessage(content=f"[From Product Agent] {response_text}")]}

def general_agent_node(state: AgentState) -> Dict:
    """Fallback agent for general greetings."""
    # Set temperature=0.5 for a friendly, conversational tone
    llm = get_llm(temperature=0.5)
    messages = state["messages"]
    sys_msg = SystemMessage(content="You are a friendly customer support agent for ShopSmart. Greet the user and ask how you can help them with their orders or finding products.")
    
    # Construct conversation history for the general agent
    convo = [sys_msg] + list(messages)
    response = llm.invoke(convo)
    
    return {"messages": [AIMessage(content=f"[From General Agent] {get_text_content(response)}")]}

# Define the edge routing logic
def route_to_agent(state: AgentState) -> str:
    return state.get("next_agent", "general")

# Build the LangGraph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("order_agent", order_agent_node)
workflow.add_node("product_agent", product_agent_node)
workflow.add_node("general", general_agent_node)

# Set the entry point
workflow.set_entry_point("supervisor")

# Add conditional edges from supervisor
workflow.add_conditional_edges(
    "supervisor",
    route_to_agent,
    {
        "order_agent": "order_agent",
        "product_agent": "product_agent",
        "general": "general"
    }
)

# All agents end the graph after they respond
workflow.add_edge("order_agent", END)
workflow.add_edge("product_agent", END)
workflow.add_edge("general", END)

# Add persistence
memory = MemorySaver()

# Compile!
app_graph = workflow.compile(checkpointer=memory)
