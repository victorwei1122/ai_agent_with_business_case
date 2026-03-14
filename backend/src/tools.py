"""
tools.py — Agent Tools
======================
Each function represents a "tool" the AI agent can invoke.
Tools are the agent's interface to external systems (databases, APIs, etc.).

Key design principles:
  1. Clear input/output contracts (JSON-like dicts)
  2. Business-rule enforcement inside the tool (not the LLM)
  3. Structured error messages the agent can reason about
"""

from datetime import datetime, timedelta
from typing import Optional

from src.mock_data import ORDERS, PRODUCTS, CUSTOMERS, SUPPORT_TICKETS


# ── Tool registry ──────────────────────────────────────────────────────────
# Maps tool names → (function, description, parameters)
# The agent uses this registry to know what tools are available.

TOOL_REGISTRY = {}


def register_tool(name: str, description: str, parameters: dict):
    """Decorator to register a function as an agent tool."""
    def decorator(func):
        TOOL_REGISTRY[name] = {
            "function": func,
            "description": description,
            "parameters": parameters,
        }
        return func
    return decorator


# ── Tool 1: Order Lookup ───────────────────────────────────────────────────

@register_tool(
    name="lookup_order",
    description="Look up an order by its ID. Returns order status, items, tracking info, and dates.",
    parameters={
        "order_id": {
            "type": "string",
            "description": "The order ID to look up (e.g. '1001')",
            "required": True,
        }
    },
)
def lookup_order(order_id: str) -> dict:
    """
    Retrieves order details from the database.

    Returns:
        dict with order info on success, or an error message.
    """
    order = ORDERS.get(order_id)
    if not order:
        return {
            "success": False,
            "error": f"Order '{order_id}' not found. Please verify the order ID.",
        }

    customer = CUSTOMERS.get(order["customer_id"], {})

    result = {
        "success": True,
        "order_id": order["id"],
        "customer_name": customer.get("name", "Unknown"),
        "status": order["status"],
        "items": order["items"],
        "total": f"${order['total']:.2f}",
        "ordered_date": order["ordered_date"],
    }

    # Add optional fields based on status
    if order.get("shipped_date"):
        result["shipped_date"] = order["shipped_date"]
    if order.get("tracking_number"):
        result["tracking_number"] = order["tracking_number"]
    if order.get("estimated_delivery"):
        result["estimated_delivery"] = order["estimated_delivery"]
    if order.get("delivered_date"):
        result["delivered_date"] = order["delivered_date"]
    if order.get("cancelled_date"):
        result["cancelled_date"] = order["cancelled_date"]
        result["cancel_reason"] = order.get("cancel_reason", "N/A")
    if order.get("returned_date"):
        result["returned_date"] = order["returned_date"]
        result["refund_status"] = order.get("refund_status", "pending")

    return result


# ── Tool 2: Process Refund ─────────────────────────────────────────────────

@register_tool(
    name="process_refund",
    description=(
        "Process a refund for an order. Checks eligibility (30-day window, valid status) "
        "and initiates the refund if eligible."
    ),
    parameters={
        "order_id": {
            "type": "string",
            "description": "The order ID to refund",
            "required": True,
        },
        "reason": {
            "type": "string",
            "description": "Reason for the refund (e.g. 'defective', 'wrong_item', 'not_satisfied')",
            "required": True,
        },
    },
)
def process_refund(order_id: str, reason: str) -> dict:
    """
    Process a refund with business-rule validation.

    Business Rules:
      - Order must exist
      - Order must be in 'delivered' status
      - Must be within 30-day return window
      - Cannot refund an already-returned order
    """
    order = ORDERS.get(order_id)
    if not order:
        return {"success": False, "error": f"Order '{order_id}' not found."}

    # Rule: Cannot refund non-delivered orders
    if order["status"] not in ("delivered",):
        status_messages = {
            "processing": "This order is still being processed and hasn't shipped yet. You can cancel it instead.",
            "shipped": "This order is currently in transit. Please wait until it's delivered to request a refund.",
            "cancelled": "This order was already cancelled.",
            "returned": "This order has already been returned and refunded.",
        }
        return {
            "success": False,
            "error": status_messages.get(
                order["status"],
                f"Order status '{order['status']}' is not eligible for a refund.",
            ),
        }

    # Rule: 30-day return window
    delivered_date = datetime.strptime(order["delivered_date"], "%Y-%m-%d")
    days_since_delivery = (datetime.now() - delivered_date).days

    if days_since_delivery > 30:
        return {
            "success": False,
            "error": (
                f"This order was delivered {days_since_delivery} days ago. "
                f"Our return policy allows refunds within 30 days of delivery."
            ),
        }

    # All checks passed — process the refund
    refund_amount = order["total"]

    return {
        "success": True,
        "order_id": order_id,
        "refund_amount": f"${refund_amount:.2f}",
        "reason": reason,
        "estimated_refund_date": (
            datetime.now() + timedelta(days=5)
        ).strftime("%Y-%m-%d"),
        "message": (
            f"Refund of ${refund_amount:.2f} has been initiated. "
            f"You should see it in your account within 5-7 business days."
        ),
    }


# ── Tool 3: Search Products ───────────────────────────────────────────────

@register_tool(
    name="search_products",
    description="Search the product catalog by keyword and/or category. Returns matching products sorted by rating.",
    parameters={
        "query": {
            "type": "string",
            "description": "Search keyword (e.g. 'laptop', 'headphones')",
            "required": False,
        },
        "category": {
            "type": "string",
            "description": "Product category filter (e.g. 'Electronics', 'Furniture')",
            "required": False,
        },
    },
)
def search_products(query: Optional[str] = None, category: Optional[str] = None) -> dict:
    """
    Search the product catalog with optional keyword and category filters.
    Results are sorted by rating (highest first).
    """
    results = []

    for product in PRODUCTS.values():
        # Apply category filter
        if category and product["category"].lower() != category.lower():
            continue

        # Apply keyword filter (searches name + description)
        if query:
            query_lower = query.lower()
            searchable = f"{product['name']} {product['description']}".lower()
            if query_lower not in searchable:
                continue

        results.append({
            "id": product["id"],
            "name": product["name"],
            "category": product["category"],
            "price": f"${product['price']:.2f}",
            "rating": f"{product['rating']}/5.0",
            "in_stock": product["in_stock"],
            "description": product["description"],
        })

    # Sort by rating descending
    results.sort(key=lambda x: float(x["rating"].split("/")[0]), reverse=True)

    if not results:
        return {
            "success": True,
            "count": 0,
            "products": [],
            "message": "No products matched your search. Try broader keywords.",
        }

    return {
        "success": True,
        "count": len(results),
        "products": results,
    }


# ── Tool 4: List Customer Orders ───────────────────────────────────────────

@register_tool(
    name="list_customer_orders",
    description="Get a list of all orders for a specific customer ID. Returns order IDs, dates, totals, and statuses.",
    parameters={
        "customer_id": {
            "type": "string",
            "description": "The customer ID to look up (e.g. 'C001')",
            "required": True,
        }
    },
)
def list_customer_orders(customer_id: str) -> dict:
    """
    Retrieves all orders for a specific customer from the mock database.
    """
    results = []
    for order_id, order in ORDERS.items():
        if order["customer_id"] == customer_id:
            results.append({
                "order_id": order["id"],
                "total": f"${order['total']:.2f}",
                "status": order["status"],
                "ordered_date": order["ordered_date"],
            })

    if not results:
        return {
            "success": False,
            "error": f"No orders found for customer ID '{customer_id}'.",
        }

    return {
        "success": True,
        "customer_id": customer_id,
        "order_count": len(results),
        "orders": results,
    }


# ── Tool 5: Escalate to Human ─────────────────────────────────────────────

@register_tool(
    name="escalate_to_human",
    description=(
        "Escalate a conversation to a human support agent. Use this for complex complaints, "
        "fraud reports, legal issues, or when the customer explicitly asks for a human."
    ),
    parameters={
        "customer_id": {
            "type": "string",
            "description": "Customer ID for the escalation",
            "required": True,
        },
        "reason": {
            "type": "string",
            "description": "Why this is being escalated (e.g. 'customer requested human', 'complex complaint')",
            "required": True,
        },
        "priority": {
            "type": "string",
            "description": "Priority level: 'low', 'normal', 'high', 'urgent'",
            "required": False,
        },
    },
)
def escalate_to_human(
    customer_id: str,
    reason: str,
    priority: str = "normal",
) -> dict:
    """
    Create an escalation ticket and transfer to a human agent.
    """
    customer = CUSTOMERS.get(customer_id)
    customer_name = customer["name"] if customer else "Unknown Customer"

    # Generate a new ticket ID
    ticket_id = f"T{len(SUPPORT_TICKETS) + 1:03d}"

    return {
        "success": True,
        "ticket_id": ticket_id,
        "customer_name": customer_name,
        "reason": reason,
        "priority": priority,
        "estimated_wait_time": "Under 5 minutes" if priority in ("high", "urgent") else "Under 15 minutes",
        "message": (
            f"I've created ticket {ticket_id} and a human agent will be with you shortly. "
            f"Estimated wait: {'under 5 minutes' if priority in ('high', 'urgent') else 'under 15 minutes'}."
        ),
    }


# ── Helper: Call a tool by name ────────────────────────────────────────────

def call_tool(tool_name: str, arguments: dict) -> dict:
    """
    Dispatch a tool call by name. This is used by the agent loop.

    Args:
        tool_name: Name of the tool to call
        arguments: Dict of keyword arguments to pass

    Returns:
        Tool result as a dict
    """
    tool = TOOL_REGISTRY.get(tool_name)
    if not tool:
        return {"success": False, "error": f"Unknown tool: '{tool_name}'"}

    try:
        return tool["function"](**arguments)
    except TypeError as e:
        return {"success": False, "error": f"Invalid arguments for '{tool_name}': {e}"}
    except Exception as e:
        return {"success": False, "error": f"Tool '{tool_name}' failed: {e}"}


def get_tools_for_prompt() -> list[dict]:
    """
    Generate the tool descriptions in the format expected by OpenAI's API.
    This is passed to the model so it knows what tools are available.
    """
    tools = []
    for name, info in TOOL_REGISTRY.items():
        properties = {}
        required = []
        for param_name, param_info in info["parameters"].items():
            properties[param_name] = {
                "type": param_info["type"],
                "description": param_info["description"],
            }
            if param_info.get("required", False):
                required.append(param_name)

        tools.append({
            "type": "function",
            "function": {
                "name": name,
                "description": info["description"],
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                },
            },
        })
    return tools
