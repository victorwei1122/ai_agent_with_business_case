from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import json
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.db.database import SessionLocal
from src.db.models import Order, Customer, Product, OrderItem
from src.prompts import SYSTEM_PROMPT
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from src.agents.llm_utils import get_llm, get_text_content, clean_tool_args

@tool
def db_lookup_order(order_id: str) -> Dict[str, Any]:
    """Look up an order by its ID. Returns order status, items, tracking info, and dates."""
    db = SessionLocal()
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            return {"success": False, "error": f"Order '{order_id}' not found. Please verify the order ID."}

        customer = db.query(Customer).filter(Customer.id == order.customer_id).first()
        
        result = {
            "success": True,
            "order_id": order.id,
            "customer_name": customer.name if customer else "Unknown",
            "status": order.status,
            "total": f"${order.total:.2f}",
            "ordered_date": order.ordered_date,
            "items": [
                {"name": item.product.name, "qty": item.qty, "price": item.price}
                for item in order.items
            ]
        }
        
        # Add optional fields
        if order.shipped_date: result["shipped_date"] = order.shipped_date
        if order.tracking_number: result["tracking_number"] = order.tracking_number
        if order.estimated_delivery: result["estimated_delivery"] = order.estimated_delivery
        if order.delivered_date: result["delivered_date"] = order.delivered_date
        if order.cancelled_date:
            result["cancelled_date"] = order.cancelled_date
            result["cancel_reason"] = order.cancel_reason or "N/A"
        if order.returned_date:
            result["returned_date"] = order.returned_date
            result["refund_status"] = order.refund_status or "pending"

        return result
    finally:
        db.close()

@tool
def db_process_refund(order_id: str, reason: str) -> Dict[str, Any]:
    """Process a refund for an order. Checks eligibility (30-day window, valid status) and initiates the refund."""
    db = SessionLocal()
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            return {"success": False, "error": f"Order '{order_id}' not found."}

        if order.status != "delivered":
            status_messages = {
                "processing": "This order is still being processed and hasn't shipped yet.",
                "shipped": "This order is currently in transit.",
                "cancelled": "This order was already cancelled.",
                "returned": "This order has already been returned and refunded.",
            }
            return {
                "success": False,
                "error": status_messages.get(order.status, f"Order status '{order.status}' is not eligible for refund.")
            }

        delivered_date = datetime.strptime(order.delivered_date, "%Y-%m-%d")
        days_since_delivery = (datetime.now() - delivered_date).days

        if days_since_delivery > 30:
            return {
                "success": False,
                "error": f"This order was delivered {days_since_delivery} days ago. Return policy allows refunds within 30 days."
            }

        refund_amount = order.total
        
        # In a real app we'd update the DB. For demo, we just return success.
        return {
            "success": True,
            "order_id": order_id,
            "refund_amount": f"${refund_amount:.2f}",
            "reason": reason,
            "estimated_refund_date": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
            "message": f"Refund of ${refund_amount:.2f} initiated. You should see it within 5-7 business days."
        }
    finally:
        db.close()

@tool
def db_get_sales_analytics(product_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Get sales figures and popularity stats for products. 
    If product_name is provided, returns sales volume for that product.
    If no product_name is provided, returns a list of top-selling products.
    """
    db = SessionLocal()
    try:
        if product_name:
            # Query for specific product sales
            # We search by name (case-insensitive)
            count = db.query(func.sum(OrderItem.qty)).join(Product).filter(Product.name.ilike(f"%{product_name}%")).scalar() or 0
            return {
                "success": True,
                "product_name": product_name,
                "total_units_sold": int(count),
                "message": f"Our records show {int(count)} units of '{product_name}' have been ordered."
            }
        else:
            # Query for top 5 best selling products
            top_sales = db.query(
                Product.id, 
                Product.name, 
                func.sum(OrderItem.qty).label('total_qty')
            ).join(OrderItem).group_by(Product.id).order_by(func.sum(OrderItem.qty).desc()).limit(5).all()
            
            results = [{"id": r[0], "name": r[1], "units_sold": int(r[2])} for r in top_sales]
            return {
                "success": True,
                "top_selling_products": results,
                "message": "Here are the top-selling products based on historical order data."
            }
    finally:
        db.close()

@tool
def db_list_customer_orders(customer_id: str) -> Dict[str, Any]:
    """Get a list of all orders for a specific customer ID. Returns order IDs, dates, and statuses."""
    db = SessionLocal()
    try:
        orders = db.query(Order).filter(Order.customer_id == customer_id).all()
        if not orders:
            return {"success": False, "error": f"No orders found for customer ID '{customer_id}'."}

        results = []
        for order in orders:
            results.append({
                "order_id": order.id,
                "total": f"${order.total:.2f}",
                "status": order.status,
                "ordered_date": order.ordered_date
            })
        
        return {
            "success": True, 
            "customer_id": customer_id, 
            "order_count": len(results),
            "orders": results
        }
    finally:
        db.close()

class TicketSchema(BaseModel):
    """Schema for creating a support ticket."""
    order_id: str = Field(description="The order ID this ticket is related to")
    subject: str = Field(description="Short summary of the issue (e.g. 'Late delivery', 'Damaged item')")
    priority: str = Field(description="Priority level: 'low', 'normal', 'high', 'urgent'")
    description: str = Field(description="Detailed explanation of the customer's problem")

@tool(args_schema=TicketSchema)
def db_create_support_ticket(order_id: str, subject: str, priority: str, description: str) -> Dict[str, Any]:
    """
    Create a new support ticket for a customer issue. 
    This is a 'Structured Tool' that requires multiple specific fields.
    """
    # In a real app, we would write to the database here.
    # For this demo, we'll return a simulated success message.
    ticket_id = "T999"  # Dummy ID
    return {
        "success": True,
        "ticket_id": ticket_id,
        "order_id": order_id,
        "subject": subject,
        "priority": priority,
        "message": f"Ticket {ticket_id} has been created and assigned to a human agent. Priority: {priority}."
    }

order_tools = [db_lookup_order, db_process_refund, db_get_sales_analytics, db_list_customer_orders, db_create_support_ticket]
def invoke_order_agent(message: str) -> str:
    """
    Invokes the Order Agent to look up orders and process refunds.
    """
    # Lazy-load LLM (Explicitly set temperature=0 for accuracy)
    llm = get_llm(temperature=0).bind_tools(order_tools)
    
    messages = [
        SystemMessage(content=SYSTEM_PROMPT + "\n\nYou are the specialized **Order Agent**. You help customers track orders, process refunds, and provide sales analytics (e.g., best-selling products or sales counts). You do NOT directly recommend products for their features, but you provide the data to back up recommendations."),
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
                
                tool_fn = next((t for t in order_tools if t.name == tool_name or t.name.endswith(tool_name)), None)
                if tool_fn:
                    tool_result = tool_fn.invoke(tool_args)
                    tool_msg = ToolMessage(content=json.dumps(tool_result), tool_call_id=tool_call["id"], name=tool_name)
                    messages.append(tool_msg)
                else:
                    messages.append(ToolMessage(content=f"Error: Tool {tool_name} not found", tool_call_id=tool_call["id"], name=tool_name))
            continue
            
        # FALLBACK: Handle text-based tool calls
        content = get_text_content(response)
        if '{"name":' in content:
            try:
                start_idx = content.find('{')
                end_idx = content.rfind('}') + 1
                tool_call_json = json.loads(content[start_idx:end_idx])
                
                tool_name = tool_call_json.get("name")
                tool_args = clean_tool_args(tool_call_json.get("parameters") or tool_call_json.get("args") or {})
                
                tool_fn = next((t for t in order_tools if t.name == tool_name or t.name.endswith(tool_name)), None)
                if tool_fn:
                    tool_result = tool_fn.invoke(tool_args)
                    tool_call_id = f"call_{len(messages)}"
                    tool_msg = ToolMessage(content=json.dumps(tool_result), tool_call_id=tool_call_id, name=tool_name)
                    messages.append(tool_msg)
                    continue
            except Exception:
                pass

        return content
                
    return "I apologize, but I am having trouble processing your order request right now."
