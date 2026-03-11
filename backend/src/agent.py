"""
agent.py — Core AI Agent with ReAct Loop
=========================================
This module implements the customer support AI agent using the ReAct
(Reasoning + Acting) pattern. It supports two modes:

  1. **OpenAI mode** — Uses GPT to reason and select tools (requires API key)
  2. **Mock mode**   — Rule-based fallback that demonstrates the same patterns

Run with:
    python -m src.agent --demo          # Run 3 demo scenarios
    python -m src.agent --interactive   # Interactive chat mode
"""

import json
import os
import re
import sys
from typing import Optional

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

from src.prompts import SYSTEM_PROMPT, MOCK_RESPONSES
from src.tools import call_tool, get_tools_for_prompt, TOOL_REGISTRY

console = Console()


# ═══════════════════════════════════════════════════════════════════════════
# Agent Core
# ═══════════════════════════════════════════════════════════════════════════

class CustomerSupportAgent:
    """
    AI-powered customer support agent using the ReAct pattern.

    The agent loop:
      1. Receive customer message
      2. THINK — Determine intent & select tool
      3. ACT   — Call the tool
      4. OBSERVE — Process tool result
      5. RESPOND — Generate customer-facing reply

    Attributes:
        conversation_history: Multi-turn message history
        use_openai: Whether to use OpenAI API (True) or mock LLM (False)
        max_tool_calls: Maximum tool calls per turn (prevent infinite loops)
    """

    def __init__(self, use_openai: bool = False, api_key: Optional[str] = None):
        self.conversation_history: list[dict] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        self.use_openai = use_openai
        self.max_tool_calls = 3
        self.client = None

        if use_openai:
            try:
                from openai import OpenAI
                
                loaded_api_key = api_key or os.getenv("OPENAI_API_KEY")
                if not loaded_api_key:
                    try:
                        import yaml
                        if os.path.exists("config.yml"):
                            with open("config.yml", "r") as f:
                                config = yaml.safe_load(f)
                                if config and getattr(config, "get", None):
                                    loaded_api_key = config.get("openai_api_key")
                    except ImportError:
                        console.print("[yellow]⚠ PyYAML not installed. Cannot read config.yml. Run pip install -r requirements.txt[/yellow]")
                    except Exception as e:
                        console.print(f"[yellow]⚠ Failed to read config.yml: {e}[/yellow]")
                        
                self.client = OpenAI(api_key=loaded_api_key)
            except ImportError:
                console.print("[yellow]⚠ openai package not installed. Falling back to mock LLM.[/yellow]")
                self.use_openai = False
            except Exception as e:
                console.print(f"[yellow]⚠ OpenAI init failed: {e}. Falling back to mock LLM.[/yellow]")
                self.use_openai = False

    # ── Main entry point ──────────────────────────────────────────────

    def chat(self, user_message: str) -> str:
        """
        Process a customer message and return the agent's response.

        This is the main ReAct loop:
          Message → Think → Act → Observe → Respond

        Args:
            user_message: The customer's message

        Returns:
            The agent's response string
        """
        # Add the user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message,
        })

        console.print(Panel(
            f"[bold cyan]Customer:[/bold cyan] {user_message}",
            border_style="cyan",
        ))

        if self.use_openai:
            response = self._openai_loop()
        else:
            response = self._mock_loop(user_message)

        # Add assistant response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": response,
        })

        # Display the response
        console.print(Panel(
            Markdown(response),
            title="🤖 SmartBot",
            border_style="green",
        ))

        return response

    # ── OpenAI-powered agent loop ─────────────────────────────────────

    def _openai_loop(self) -> str:
        """
        ReAct loop using OpenAI's function calling API.

        The model decides which tool to call (if any), we execute the tool,
        feed the result back, and let the model generate the final response.
        """
        tools = get_tools_for_prompt()
        tool_calls_made = 0

        while tool_calls_made < self.max_tool_calls:
            # Call OpenAI with current conversation + tools
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=self.conversation_history,
                tools=tools,
                tool_choice="auto",
            )

            message = response.choices[0].message

            # If the model wants to call a tool
            if message.tool_calls:
                # Add the assistant's tool-call message to history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": message.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments,
                            },
                        }
                        for tc in message.tool_calls
                    ],
                })

                # Execute each tool call
                for tc in message.tool_calls:
                    tool_name = tc.function.name
                    arguments = json.loads(tc.function.arguments)

                    # ── THINK ──
                    console.print(f"  [dim]💭 Think: Calling {tool_name}({arguments})[/dim]")

                    # ── ACT ──
                    result = call_tool(tool_name, arguments)
                    tool_calls_made += 1

                    # ── OBSERVE ──
                    console.print(f"  [dim]👁  Observe: {json.dumps(result, indent=2)[:200]}...[/dim]")

                    # Add tool result to history
                    self.conversation_history.append({
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": json.dumps(result),
                    })
            else:
                # ── RESPOND — No more tool calls, return the final response ──
                return message.content

        # Fallback if we hit the tool call limit
        return "I apologize, but I'm having trouble resolving your issue. Let me connect you with a human agent."

    # ── Mock LLM (rule-based fallback) ────────────────────────────────

    def _mock_loop(self, user_message: str) -> str:
        """
        Rule-based agent that simulates the same ReAct pattern without an LLM.

        This demonstrates the SAME tool-calling architecture — the only
        difference is intent detection is done with keyword matching instead
        of an LLM.

        This is intentionally simple to highlight the architecture, not to
        build a production-ready NLP system.
        """
        msg = user_message.lower().strip()

        # ── Intent Detection (replaces LLM reasoning) ────────────────

        # Greeting
        if any(w in msg for w in ("hello", "hi", "hey", "help", "start")):
            if len(msg.split()) <= 3:  # Short greeting only
                return MOCK_RESPONSES["greeting"]

        # Escalation request
        if any(phrase in msg for phrase in ("human", "real person", "speak to someone", "manager")):
            console.print("  [dim]💭 Think: Customer wants a human agent → escalate[/dim]")
            result = call_tool("escalate_to_human", {
                "customer_id": "C001",
                "reason": "Customer requested human agent",
                "priority": "normal",
            })
            console.print(f"  [dim]👁  Observe: {result}[/dim]")
            return MOCK_RESPONSES["escalation"].format(**result)

        # Order lookup
        order_match = re.search(r'(?:order|#)\s*(\d{4})', msg)
        if order_match or any(w in msg for w in ("order", "tracking", "where is", "status", "delivery")):
            order_id = order_match.group(1) if order_match else "1001"

            console.print(f"  [dim]💭 Think: Customer asking about order → lookup_order({order_id})[/dim]")
            result = call_tool("lookup_order", {"order_id": order_id})
            console.print(f"  [dim]👁  Observe: {json.dumps(result, indent=2)[:200]}...[/dim]")

            if not result["success"]:
                return f"I couldn't find order #{order_id}. Could you double-check the order number?"

            # Check if they want a refund
            if any(w in msg for w in ("refund", "return", "money back")):
                console.print(f"  [dim]💭 Think: Customer wants refund → process_refund({order_id})[/dim]")
                refund_result = call_tool("process_refund", {
                    "order_id": order_id,
                    "reason": "customer_request",
                })
                console.print(f"  [dim]👁  Observe: {json.dumps(refund_result, indent=2)[:200]}...[/dim]")

                if refund_result["success"]:
                    return MOCK_RESPONSES["refund_success"].format(**refund_result)
                else:
                    return MOCK_RESPONSES["refund_denied"].format(
                        order_id=order_id, **refund_result
                    )

            # Build extra info based on status
            extra = ""
            if result["status"] == "shipped":
                extra = (
                    f"🚚 **Tracking**: {result.get('tracking_number', 'N/A')}\n"
                    f"📅 **Estimated delivery**: {result.get('estimated_delivery', 'N/A')}\n"
                )
            elif result["status"] == "delivered":
                extra = f"✅ **Delivered on**: {result.get('delivered_date', 'N/A')}\n"
            elif result["status"] == "processing":
                extra = "⏳ Your order is being prepared and will ship soon.\n"
            elif result["status"] == "cancelled":
                extra = f"❌ **Cancelled**: {result.get('cancel_reason', 'N/A')}\n"

            items_str = ", ".join(
                f"{item['name']} (x{item['qty']})" for item in result["items"]
            )

            return MOCK_RESPONSES["order_status"].format(
                order_id=result["order_id"],
                status=result["status"].title(),
                items=items_str,
                total=result["total"],
                extra_info=extra,
            )

        # Refund without order number
        if any(w in msg for w in ("refund", "return", "money back")):
            return (
                "I'd be happy to help with a refund! "
                "Could you please provide your order number? "
                "It usually starts with a 4-digit number like #1001."
            )

        # Product search
        if any(w in msg for w in ("recommend", "suggest", "looking for", "buy", "product", "laptop", "headphone", "desk", "chair", "keyboard", "monitor")):
            # Extract likely search terms
            search_terms = []
            category = None
            for word in ("laptop", "headphone", "keyboard", "monitor", "desk", "chair", "backpack"):
                if word in msg:
                    search_terms.append(word)
            if any(w in msg for w in ("desk", "chair")):
                category = "Furniture"
            elif any(w in msg for w in ("laptop", "headphone", "keyboard", "monitor")):
                category = "Electronics"

            query = search_terms[0] if search_terms else None

            console.print(f"  [dim]💭 Think: Customer wants product recommendations → search_products(query={query}, category={category})[/dim]")
            result = call_tool("search_products", {"query": query, "category": category})
            console.print(f"  [dim]👁  Observe: Found {result['count']} products[/dim]")

            if result["count"] == 0:
                return MOCK_RESPONSES["no_products"]

            product_lines = []
            for p in result["products"][:5]:  # Show max 5
                stock = "✅ In Stock" if p["in_stock"] else "❌ Out of Stock"
                product_lines.append(
                    f"- **{p['name']}** — {p['price']} | ⭐ {p['rating']} | {stock}\n"
                    f"  _{p['description']}_"
                )

            return MOCK_RESPONSES["product_results"].format(
                product_list="\n".join(product_lines)
            )

        # Fallback
        return MOCK_RESPONSES["fallback"]


# ═══════════════════════════════════════════════════════════════════════════
# Demo Scenarios
# ═══════════════════════════════════════════════════════════════════════════

DEMO_SCENARIOS = [
    {
        "title": "📦 Scenario 1: Order Status Inquiry",
        "description": "Customer asks where their order is.",
        "messages": [
            "Hi, I placed an order a few days ago. Can you tell me where order #1001 is?",
        ],
    },
    {
        "title": "💰 Scenario 2: Refund Request",
        "description": "Customer wants to return headphones from order #1002.",
        "messages": [
            "I'd like to return the headphones from order #1002 and get a refund please.",
        ],
    },
    {
        "title": "🛍️ Scenario 3: Product Recommendation",
        "description": "Customer looking for a laptop for coding.",
        "messages": [
            "Can you recommend a good laptop for coding?",
        ],
    },
]


def run_demo():
    """Run the built-in demo scenarios to showcase the agent."""
    console.print(Panel(
        "[bold]🤖 AI Customer Support Agent — Demo Mode[/bold]\n\n"
        "Running 3 realistic customer scenarios to demonstrate\n"
        "the ReAct (Reasoning + Acting) agent pattern.\n\n"
        "[dim]Mode: Mock LLM (no API key required)[/dim]",
        border_style="blue",
        title="ShopSmart Support",
    ))

    agent = CustomerSupportAgent(use_openai=False)

    for i, scenario in enumerate(DEMO_SCENARIOS, 1):
        console.print()
        console.rule(f"[bold yellow]{scenario['title']}[/bold yellow]")
        console.print(f"[dim]{scenario['description']}[/dim]\n")

        for message in scenario["messages"]:
            agent.chat(message)
            console.print()

        # Reset conversation for next scenario
        agent.conversation_history = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    console.print(Panel(
        "[bold green]✅ Demo complete![/bold green]\n\n"
        "To explore more:\n"
        "  • Run [bold]python -m src.agent --interactive[/bold] for a chat session\n"
        "  • Open [bold]notebooks/tutorial.ipynb[/bold] for the full walkthrough\n"
        "  • Update [bold]config.yml[/bold] with your OPENAI_API_KEY to use GPT instead of the mock LLM",
        border_style="green",
    ))


def run_interactive():
    """Run an interactive chat session with the agent."""
    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        try:
            import yaml
            if os.path.exists("config.yml"):
                with open("config.yml", "r") as f:
                    config = yaml.safe_load(f)
                    if config and getattr(config, "get", None):
                        api_key = config.get("openai_api_key")
        except ImportError:
            pass
        except Exception:
            pass

    use_openai = bool(api_key)

    mode_str = "OpenAI GPT" if use_openai else "Mock LLM (set openai_api_key in config.yml for GPT)"

    console.print(Panel(
        f"[bold]🤖 AI Customer Support Agent — Interactive Mode[/bold]\n\n"
        f"Mode: {mode_str}\n"
        f"Type [bold]quit[/bold] to exit.\n\n"
        f"[dim]Try: 'Where is my order #1001?' or 'I want to return order #1002'[/dim]",
        border_style="blue",
        title="ShopSmart Support",
    ))

    agent = CustomerSupportAgent(use_openai=use_openai, api_key=api_key)

    while True:
        try:
            user_input = console.input("\n[bold cyan]You:[/bold cyan] ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("quit", "exit", "bye", "q"):
                console.print("\n[green]Thanks for chatting! Have a great day! 👋[/green]")
                break
            agent.chat(user_input)
        except KeyboardInterrupt:
            console.print("\n[green]Goodbye! 👋[/green]")
            break


# ═══════════════════════════════════════════════════════════════════════════
# CLI Entry Point
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if "--demo" in sys.argv:
        run_demo()
    elif "--interactive" in sys.argv:
        run_interactive()
    else:
        console.print(
            "Usage:\n"
            "  python -m src.agent --demo          Run 3 demo scenarios\n"
            "  python -m src.agent --interactive    Interactive chat session\n"
        )
