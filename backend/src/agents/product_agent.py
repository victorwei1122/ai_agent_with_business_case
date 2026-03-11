import json
from typing import Dict, Any, Optional
from langchain_core.tools import tool
from sqlalchemy.orm import Session
from src.db.database import SessionLocal
from src.db.models import Product
from src.prompts import SYSTEM_PROMPT
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from src.agents.llm_utils import get_llm, get_text_content, clean_tool_args

@tool
def db_search_products(query: Optional[str] = None, category: Optional[str] = None) -> Dict[str, Any]:
    """Search the product catalog by keyword and/or category. Returns matching products."""
    db = SessionLocal()
    try:
        q = db.query(Product)
        
        if category:
            q = q.filter(Product.category.ilike(f"%{category}%"))
            
        if query:
            # Simple keyword splitting for better matching (e.g., "ProBook 15" -> ["ProBook", "15"])
            keywords = query.split()
            for kw in keywords:
                search_pattern = f"%{kw}%"
                q = q.filter(
                    (Product.name.ilike(search_pattern)) | 
                    (Product.description.ilike(search_pattern)) |
                    (Product.tags.ilike(search_pattern))
                )
            
        products = q.order_by(Product.rating.desc()).limit(5).all()
        
        results = []
        for p in products:
            results.append({
                "id": p.id,
                "name": p.name,
                "brand": p.brand,
                "category": p.category,
                "price": f"${p.price:.2f}",
                "rating": f"{p.rating}/5.0",
                "in_stock": p.in_stock,
                "description": p.description,
                "specs": p.specs,
                "warranty": p.warranty,
                "tags": p.tags,
            })
            
        if not results:
            return {
                "success": True,
                "count": 0,
                "products": [],
                "message": "No products matched your search. Try broader keywords."
            }

        return {
            "success": True,
            "count": len(results),
            "products": results,
        }
    finally:
        db.close()

@tool
def db_get_product_reviews(product_id: str) -> Dict[str, Any]:
    """Get customer reviews for a specific product ID. Returns a list of comments and ratings."""
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return {"success": False, "error": "Product not found"}
            
        reviews = []
        for r in product.reviews:
            reviews.append({
                "customer": r.customer_name,
                "rating": f"{r.rating}/5",
                "comment": r.comment,
                "date": r.date
            })
            
        return {
            "success": True,
            "product_name": product.name,
            "reviews": reviews
        }
    finally:
        db.close()

product_tools = [db_search_products, db_get_product_reviews]
def invoke_product_agent(message: str) -> str:
    """
    Invokes the Product Agent to search for products and recommend them.
    """
    # Lazy-load LLM to avoid module-level side effects
    llm = get_llm().bind_tools(product_tools)
    
    messages = [
        SystemMessage(content=SYSTEM_PROMPT + "\n\nYou are the specialized **Product Agent**. You help customers find laptops, headphones, desks, and other items to buy. You do NOT look up orders or process refunds."),
        HumanMessage(content=message)
    ]
    
    for i in range(5):
        response = llm.invoke(messages)
        messages.append(response)
        
        # EXECUTION: Handle structured tool calls
        if response.tool_calls:
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = clean_tool_args(tool_call["args"])
                
                tool_fn = next((t for t in product_tools if t.name == tool_name or t.name.endswith(tool_name)), None)
                if tool_fn:
                    tool_result = tool_fn.invoke(tool_args)
                    tool_msg = ToolMessage(content=json.dumps(tool_result), tool_call_id=tool_call["id"], name=tool_name)
                    messages.append(tool_msg)
                else:
                    messages.append(ToolMessage(content=f"Error: Tool {tool_name} not found", tool_call_id=tool_call["id"], name=tool_name))
            continue # Go to next iteration to let model process tool results
            
        # FALLBACK: Handle text-based tool calls (common with smaller local models)
        content = get_text_content(response)
        if '{"name":' in content:
            try:
                # Find the JSON part
                start_idx = content.find('{')
                end_idx = content.rfind('}') + 1
                tool_call_json = json.loads(content[start_idx:end_idx])
                
                tool_name = tool_call_json.get("name")
                tool_args = clean_tool_args(tool_call_json.get("parameters") or tool_call_json.get("args") or {})
                
                tool_fn = next((t for t in product_tools if t.name == tool_name or t.name.endswith(tool_name)), None)
                if tool_fn:
                    tool_result = tool_fn.invoke(tool_args)
                    # We need a fake tool_call_id for the message history
                    tool_call_id = f"call_{len(messages)}"
                    tool_msg = ToolMessage(content=json.dumps(tool_result), tool_call_id=tool_call_id, name=tool_name)
                    messages.append(tool_msg)
                    continue
            except Exception:
                pass
                
        return content
                
    return "I apologize, but I am having trouble recommending products right now."
