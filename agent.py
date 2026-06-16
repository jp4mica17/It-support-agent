"""
agent.py — IT Support Agent

Orchestrates an agentic loop using Claude + tool use:
  1. User sends a message
  2. Claude decides which tool(s) to call (search KB, create ticket, escalate)
  3. Tool results are fed back to Claude
  4. Claude generates a final, grounded response

The agent is stateless between calls; conversation history is passed in
from the Streamlit session state on every turn.
"""

import os
import json

import anthropic
from dotenv import load_dotenv

from rag import RAGRetriever
from tools import create_servicenow_ticket, escalate_to_human

load_dotenv()


# ──────────────────────────────────────────────
# Tool schema definitions (sent to Claude)
# ──────────────────────────────────────────────

TOOLS = [
    {
        "name": "search_knowledge_base",
        "description": (
            "Search the IT knowledge base for articles relevant to the user's issue. "
            "ALWAYS call this first before considering any other action."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A clear, specific search query describing the IT issue.",
                },
                "n_results": {
                    "type": "integer",
                    "description": "Number of articles to retrieve. Default 3, max 5.",
                    "default": 3,
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "create_servicenow_ticket",
        "description": (
            "Create a ServiceNow incident ticket when the issue cannot be resolved "
            "via KB articles alone, or when hands-on IT access is required."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Short, clear title describing the issue.",
                },
                "description": {
                    "type": "string",
                    "description": "Detailed description including steps already attempted.",
                },
                "priority": {
                    "type": "string",
                    "enum": ["1-Critical", "2-High", "3-Medium", "4-Low"],
                    "description": "Priority based on business impact.",
                },
                "category": {
                    "type": "string",
                    "enum": [
                        "Hardware",
                        "Software",
                        "Network",
                        "Access/Identity",
                        "Email",
                        "Other",
                    ],
                },
            },
            "required": ["title", "description", "priority", "category"],
        },
    },
    {
        "name": "escalate_to_human",
        "description": (
            "Immediately escalate to the on-call IT analyst. Use for: "
            "security incidents (phishing, malware, breach), exec/VIP support emergencies, "
            "full system or network outages affecting multiple users."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "reason": {
                    "type": "string",
                    "description": "Why this requires immediate human intervention.",
                },
                "severity": {
                    "type": "string",
                    "enum": ["Critical", "High"],
                },
            },
            "required": ["reason", "severity"],
        },
    },
]


SYSTEM_PROMPT = """You are an expert IT support analyst at a large enterprise.
Your job is to help employees resolve IT issues quickly and accurately.

Guidelines:
- ALWAYS search the knowledge base first before any other action.
- If KB articles contain the answer, give a clear, numbered step-by-step resolution.
- Only create a ticket if the issue genuinely requires hands-on IT work or cannot be self-resolved.
- Escalate immediately for: security incidents, executive emergencies, or widespread outages.
- Be professional, empathetic, and specific — avoid vague answers.
- If you created a ticket or escalated, clearly tell the user what to expect next.
"""


# ──────────────────────────────────────────────
# Agent class
# ──────────────────────────────────────────────


class ITSupportAgent:
    def __init__(self):
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not set. Copy .env.example → .env and add your key."
            )
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-6")
        self.retriever = RAGRetriever()

    # ── internal helpers ──

    def _block_to_dict(self, block) -> dict:
        """Convert an Anthropic content block object to a plain dict."""
        if block.type == "text":
            return {"type": "text", "text": block.text}
        elif block.type == "tool_use":
            return {
                "type": "tool_use",
                "id": block.id,
                "name": block.name,
                "input": block.input,
            }
        return {}

    def _run_tool(self, name: str, inputs: dict) -> tuple[str, dict]:
        """
        Execute a tool by name.
        Returns (result_string_for_claude, metadata_dict_for_ui).
        """
        metadata = {}

        if name == "search_knowledge_base":
            n = inputs.get("n_results", 3)
            articles = self.retriever.search(inputs["query"], n_results=n)
            metadata["kb_articles"] = articles

            if not articles:
                return "No relevant KB articles found for that query.", metadata

            parts = []
            for i, a in enumerate(articles, 1):
                parts.append(
                    f"[Article {i}] {a['title']} (relevance: {a['score']})\n{a['content']}"
                )
            return "\n\n---\n\n".join(parts), metadata

        elif name == "create_servicenow_ticket":
            ticket = create_servicenow_ticket(**inputs)
            metadata["ticket"] = ticket
            return json.dumps(ticket, indent=2), metadata

        elif name == "escalate_to_human":
            result = escalate_to_human(**inputs)
            metadata["escalation"] = result
            return json.dumps(result, indent=2), metadata

        return f"Unknown tool: {name}", metadata

    # ── public API ──

    def chat(self, user_message: str, history: list[dict]) -> dict:
        """
        Process one user turn.

        Args:
            user_message: The user's latest message.
            history: Prior conversation as [{"role": ..., "content": ...}, ...].
                     Only string content; tool-use turns are managed internally.

        Returns a dict:
            response     str   — Final text to show the user
            kb_articles  list  — KB chunks retrieved (for sidebar)
            ticket       dict  — Ticket created, or None
            escalation   dict  — Escalation record, or None
            tools_used   list  — Names of tools called this turn
        """
        # Build the messages array from simple text history
        messages = [
            {"role": m["role"], "content": m["content"]}
            for m in history
            if m.get("role") in ("user", "assistant") and isinstance(m.get("content"), str)
        ]
        messages.append({"role": "user", "content": user_message})

        # Accumulated metadata across the agentic loop
        all_kb_articles: list = []
        all_tickets: list = []
        escalation = None
        tools_used: list = []

        # ── Agentic loop ──
        max_iterations = 8  # safety ceiling
        for _ in range(max_iterations):
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                system=SYSTEM_PROMPT,
                tools=TOOLS,
                messages=messages,
            )

            if response.stop_reason == "end_turn":
                # Extract the final text response
                final_text = "".join(
                    b.text for b in response.content if b.type == "text"
                )
                return {
                    "response": final_text,
                    "kb_articles": all_kb_articles,
                    "ticket": all_tickets[-1] if all_tickets else None,
                    "escalation": escalation,
                    "tools_used": tools_used,
                }

            elif response.stop_reason == "tool_use":
                tool_results = []

                for block in response.content:
                    if block.type != "tool_use":
                        continue

                    tools_used.append(block.name)
                    result_str, meta = self._run_tool(block.name, block.input)

                    # Accumulate metadata
                    if "kb_articles" in meta:
                        all_kb_articles = meta["kb_articles"]
                    if "ticket" in meta:
                        all_tickets.append(meta["ticket"])
                    if "escalation" in meta:
                        escalation = meta["escalation"]

                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result_str,
                        }
                    )

                # Append assistant turn (all blocks) + tool results
                messages.append(
                    {
                        "role": "assistant",
                        "content": [self._block_to_dict(b) for b in response.content],
                    }
                )
                messages.append({"role": "user", "content": tool_results})

            else:
                break

        return {
            "response": "I ran into an unexpected issue. Please try again.",
            "kb_articles": all_kb_articles,
            "ticket": None,
            "escalation": None,
            "tools_used": tools_used,
        }
