"""
evals/run_evals.py — Evaluation Harness for the IT Support Agent

Runs 20 test cases through the agent and scores them on:
  1. Tool accuracy    — did the agent call the expected tools?
  2. Ticket accuracy  — did it create/skip tickets correctly?
  3. Escalation accuracy — did it escalate when it should?
  4. Response quality — LLM-as-judge (Claude Haiku) scores 1–5

Usage (from the project root):
    python evals/run_evals.py

Results are saved to evals/results.json and printed as a table.
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Add parent directory to path so we can import agent
sys.path.insert(0, str(Path(__file__).parent.parent))

import anthropic
from dotenv import load_dotenv
from tabulate import tabulate

from agent import ITSupportAgent

load_dotenv()

JUDGE_MODEL = "claude-haiku-4-5-20251001"
RESULTS_PATH = Path(__file__).parent / "results.json"
CASES_PATH = Path(__file__).parent / "test_cases.json"


# ── LLM-as-judge ──────────────────────────────────────────────────────────────

JUDGE_PROMPT = """You are evaluating an IT support AI agent's response.

User query: {query}

Agent response: {response}

Score the response on a scale of 1–5:
  5 — Excellent: accurate, specific, actionable, empathetic
  4 — Good: mostly correct with minor gaps
  3 — Adequate: correct but vague or missing key steps
  2 — Poor: partially correct or confusing
  1 — Bad: wrong, unhelpful, or hallucinates

Respond with ONLY a JSON object, nothing else:
{{"score": <1-5>, "reason": "<one sentence>"}}"""


def judge_response(client: anthropic.Anthropic, query: str, response: str) -> dict:
    """Use Claude Haiku to score the agent's response quality."""
    try:
        result = client.messages.create(
            model=JUDGE_MODEL,
            max_tokens=150,
            messages=[
                {
                    "role": "user",
                    "content": JUDGE_PROMPT.format(query=query, response=response),
                }
            ],
        )
        text = result.content[0].text.strip()
        # Strip markdown fences if present
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        return {"score": 0, "reason": f"Judge error: {e}"}


# ── Scoring helpers ────────────────────────────────────────────────────────────

def score_tools(tools_used: list[str], expected_tools: list[str]) -> tuple[bool, str]:
    """
    Check if the critical expected tools were all called.
    search_knowledge_base is treated as 'almost always expected unless escalating'.
    """
    tools_set = set(tools_used)
    expected_set = set(expected_tools)

    # We don't penalise for calling extra tools (e.g. KB search + ticket)
    missing = expected_set - tools_set
    if not missing:
        return True, "All expected tools called"
    return False, f"Missing: {', '.join(missing)}"


def score_ticket(created: bool, should_create: bool) -> bool:
    return created == should_create


def score_escalation(escalated: bool, should_escalate: bool) -> bool:
    return escalated == should_escalate


# ── Main eval loop ─────────────────────────────────────────────────────────────

def run_evals():
    print("=" * 60)
    print("  IT Support Agent — Evaluation Run")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    with open(CASES_PATH) as f:
        test_cases = json.load(f)

    agent = ITSupportAgent()
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    rows = []
    results = []
    total_quality = 0
    total_tool = 0
    total_ticket = 0
    total_escalation = 0

    for i, case in enumerate(test_cases, 1):
        print(f"\n[{i:02d}/{len(test_cases)}] {case['id']} — {case['query'][:60]}…")

        try:
            result = agent.chat(case["query"], [])
            time.sleep(0.5)  # gentle rate-limiting

            tools_used = result.get("tools_used", [])
            ticket_created = result.get("ticket") is not None
            escalated = result.get("escalation") is not None
            response = result.get("response", "")

            # Score dimensions
            tool_pass, tool_note = score_tools(tools_used, case["expected_tools"])
            ticket_pass = score_ticket(ticket_created, case["should_create_ticket"])
            escalation_pass = score_escalation(escalated, case["should_escalate"])

            # LLM-as-judge quality score
            judgment = judge_response(client, case["query"], response)
            quality_score = judgment.get("score", 0)
            quality_reason = judgment.get("reason", "")
            time.sleep(0.3)

            # Accumulate
            total_quality += quality_score
            total_tool += int(tool_pass)
            total_ticket += int(ticket_pass)
            total_escalation += int(escalation_pass)

            overall_pass = tool_pass and ticket_pass and escalation_pass
            status = "✅ PASS" if overall_pass else "❌ FAIL"

            rows.append([
                case["id"],
                case["difficulty"],
                case["category"],
                status,
                "✅" if tool_pass else f"❌ {tool_note}",
                "✅" if ticket_pass else "❌",
                "✅" if escalation_pass else "❌",
                f"{quality_score}/5",
            ])

            results.append({
                **case,
                "tools_used": tools_used,
                "ticket_created": ticket_created,
                "escalated": escalated,
                "tool_pass": tool_pass,
                "ticket_pass": ticket_pass,
                "escalation_pass": escalation_pass,
                "quality_score": quality_score,
                "quality_reason": quality_reason,
                "response_preview": response[:200],
            })

            print(f"         Tools: {', '.join(tools_used) or 'none'}")
            print(f"         Quality: {quality_score}/5 — {quality_reason}")
            print(f"         Result: {status}")

        except Exception as e:
            print(f"         ERROR: {e}")
            rows.append([case["id"], case["difficulty"], case["category"], "💥 ERROR",
                         "-", "-", "-", "-"])
            results.append({**case, "error": str(e)})

    # ── Summary ────────────────────────────────────────────────────────────────
    n = len(test_cases)
    print("\n" + "=" * 60)
    print("  RESULTS")
    print("=" * 60)
    print(tabulate(
        rows,
        headers=["ID", "Difficulty", "Category", "Status", "Tools", "Ticket", "Escalation", "Quality"],
        tablefmt="rounded_outline",
    ))

    print(f"""
Summary
-------
Total cases:       {n}
Tool accuracy:     {total_tool}/{n}  ({total_tool/n*100:.0f}%)
Ticket accuracy:   {total_ticket}/{n}  ({total_ticket/n*100:.0f}%)
Escalation acc.:   {total_escalation}/{n}  ({total_escalation/n*100:.0f}%)
Avg quality:       {total_quality/n:.2f}/5.0
""")

    # Save full results
    output = {
        "run_at": datetime.now().isoformat(),
        "model": agent.model,
        "judge_model": JUDGE_MODEL,
        "summary": {
            "n": n,
            "tool_accuracy": round(total_tool / n, 3),
            "ticket_accuracy": round(total_ticket / n, 3),
            "escalation_accuracy": round(total_escalation / n, 3),
            "avg_quality": round(total_quality / n, 2),
        },
        "cases": results,
    }
    with open(RESULTS_PATH, "w") as f:
        json.dump(output, f, indent=2)
    print(f"Full results saved to: {RESULTS_PATH}")


if __name__ == "__main__":
    run_evals()
