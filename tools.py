"""
tools.py — Tool implementations callable by the IT Support Agent

These functions are invoked when the LLM decides to use a tool.
In production these would call real ServiceNow / PagerDuty APIs.
For this portfolio demo, they return realistic mock responses.
"""

import random
import string
from datetime import datetime


def create_servicenow_ticket(
    title: str,
    description: str,
    priority: str,
    category: str,
) -> dict:
    """
    Create a mock ServiceNow incident ticket.

    Priority levels:
      1-Critical  → 1 hour SLA
      2-High      → 4 hours SLA
      3-Medium    → 1 business day SLA
      4-Low       → 3 business days SLA
    """
    ticket_number = "INC" + "".join(random.choices(string.digits, k=7))

    sla_map = {
        "1-Critical": "1 hour",
        "2-High": "4 hours",
        "3-Medium": "1 business day",
        "4-Low": "3 business days",
    }

    return {
        "number": ticket_number,
        "title": title,
        "description": description,
        "priority": priority,
        "category": category,
        "status": "New",
        "assigned_to": "IT Support Queue",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "sla_target": sla_map.get(priority, "1 business day"),
    }


def escalate_to_human(reason: str, severity: str) -> dict:
    """
    Immediately escalate to the on-call IT analyst.

    Used for: security incidents, exec support, widespread outages,
    or any situation where the agent cannot safely resolve the issue.
    """
    escalation_id = "ESC" + "".join(random.choices(string.digits, k=5))
    response_time = "15 minutes" if severity == "Critical" else "30 minutes"

    return {
        "escalation_id": escalation_id,
        "severity": severity,
        "reason": reason,
        "assigned_to": "On-Call IT Analyst",
        "estimated_response": response_time,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "contact_channel": "Slack #it-oncall | Phone ext. 5555",
    }
