from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
import traceback
import logging

# Pydantic models for request/response
class ChatRequest(BaseModel):
    message: str
    customer_id: Optional[str] = "C001" # Defaulting for demo purposes

class ChatResponse(BaseModel):
    response: str
    sub_agent_used: str

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ShopSmart AI Microservices", version="1.0.0")

# Allow requests from the Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Placeholder for now, we will add routes later
@app.get("/health")
def health_check():
    return {"status": "ok"}

from src.agents.order_agent import invoke_order_agent
from src.agents.product_agent import invoke_product_agent

@app.post("/agent/order", response_model=ChatResponse)
def order_agent_endpoint(request: ChatRequest):
    """Dedicated endpoint for the Order Agent"""
    try:
        reply = invoke_order_agent(request.message)
        return ChatResponse(response=reply, sub_agent_used="Order Agent")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/agent/product", response_model=ChatResponse)
def product_agent_endpoint(request: ChatRequest):
    """Dedicated endpoint for the Product Agent"""
    try:
        reply = invoke_product_agent(request.message)
        return ChatResponse(response=reply, sub_agent_used="Product Agent")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


import traceback
from langchain_core.messages import HumanMessage
from src.graph import app_graph
from src.agents.llm_utils import get_text_content

@app.post("/chat", response_model=ChatResponse)
async def orchestration_endpoint(request: ChatRequest):
    """The main entry point using LangGraph to route to the correct agent."""
    try:
        # 1. Run the LangGraph orchestration
        state = {"messages": [HumanMessage(content=request.message)]}
        result = app_graph.invoke(state)
        
        # 2. Extract final response from the graph's messages
        if result and result.get("messages"):
            last_message = result["messages"][-1]
            sub_agent = result.get("next_agent", "supervisor")

            return ChatResponse(
                response=get_text_content(last_message),
                sub_agent_used=sub_agent
            )
        else:
            return ChatResponse(response="I'm sorry, an error occurred processing your request.", sub_agent_used="error")
            
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
