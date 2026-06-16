"""
app.py — IT Support Agent — Streamlit UI

Run with:  streamlit run app.py
"""

import streamlit as st
from agent import ITSupportAgent
from rag import RAGRetriever

# ──────────────────────────────────────────────
# Page config
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="IT Support Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# Custom CSS — clean, enterprise-style theme
# ──────────────────────────────────────────────
st.markdown(
    """
    <style>
        /* Page background */
        .stApp { background-color: #f8f9fa; }

        /* Main content area */
        section.main > div { padding-top: 1.5rem; }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #1a1f2e;
            color: #e2e8f0;
        }
        [data-testid="stSidebar"] * { color: #e2e8f0 !important; }
        [data-testid="stSidebar"] .stExpander {
            background-color: #252c3f;
            border: 1px solid #374151;
            border-radius: 8px;
        }

        /* Chat bubbles */
        [data-testid="stChatMessage"] {
            border-radius: 12px;
            margin-bottom: 0.5rem;
            background-color: #ffffff;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        }

        /* Ticket badge */
        .ticket-badge {
            background-color: #10b981;
            color: white;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 0.85rem;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 6px;
        }

        /* Escalation badge */
        .escalation-badge {
            background-color: #ef4444;
            color: white;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 0.85rem;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 6px;
        }

        /* Tool chip */
        .tool-chip {
            background-color: #e0e7ff;
            color: #3730a3;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 500;
            display: inline-block;
            margin: 2px 3px;
        }

        /* Score bar */
        .score-bar {
            height: 4px;
            border-radius: 2px;
            background: linear-gradient(90deg, #6366f1, #8b5cf6);
            margin-bottom: 8px;
        }

        /* Header */
        .agent-header {
            background: linear-gradient(135deg, #1a1f2e 0%, #2d3748 100%);
            border-radius: 12px;
            padding: 20px 24px;
            margin-bottom: 20px;
            color: white;
        }
        .agent-header h1 { color: white !important; margin: 0; font-size: 1.6rem; }
        .agent-header p { color: #94a3b8 !important; margin: 4px 0 0 0; font-size: 0.9rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ──────────────────────────────────────────────
# Cached resource initialisation
# ──────────────────────────────────────────────

@st.cache_resource(show_spinner="Loading agent…")
def load_agent():
    return ITSupportAgent()


@st.cache_resource(show_spinner=False)
def load_retriever():
    return RAGRetriever()


# ──────────────────────────────────────────────
# Guard: KB must be ingested first
# ──────────────────────────────────────────────

retriever = load_retriever()
if not retriever.is_ready():
    with st.spinner("⚙️ Setting up knowledge base (first run only — takes about 2 minutes)…"):
        from ingest import ingest
        ingest()
    st.rerun()

agent = load_agent()


# ──────────────────────────────────────────────
# Session state
# ──────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_kb_articles" not in st.session_state:
    st.session_state.last_kb_articles = []
if "tickets" not in st.session_state:
    st.session_state.tickets = []
if "last_escalation" not in st.session_state:
    st.session_state.last_escalation = None
if "last_tools_used" not in st.session_state:
    st.session_state.last_tools_used = []


# ──────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────

with st.sidebar:
    st.markdown("### 🤖 IT Support Agent")
    st.caption("Claude + RAG | Portfolio Demo")
    st.divider()

    # Tools used
    if st.session_state.last_tools_used:
        st.markdown("**🔧 Tools called this turn**")
        tool_labels = {
            "search_knowledge_base": "🔍 KB Search",
            "create_servicenow_ticket": "🎫 Create Ticket",
            "escalate_to_human": "🚨 Escalate",
        }
        chips = " ".join(
            f'<span class="tool-chip">{tool_labels.get(t, t)}</span>'
            for t in st.session_state.last_tools_used
        )
        st.markdown(chips, unsafe_allow_html=True)
        st.markdown("")

    # KB articles
    st.markdown("**📚 Retrieved KB Articles**")
    if st.session_state.last_kb_articles:
        for article in st.session_state.last_kb_articles:
            pct = int(article["score"] * 100)
            with st.expander(f"{article['title']} — {pct}% match"):
                st.markdown(
                    f'<div class="score-bar" style="width:{pct}%"></div>',
                    unsafe_allow_html=True,
                )
                st.write(article["content"])
    else:
        st.caption("No articles retrieved yet.")

    st.divider()

    # Tickets
    st.markdown("**🎫 ServiceNow Tickets**")
    if st.session_state.tickets:
        for t in reversed(st.session_state.tickets):
            st.markdown(
                f'<span class="ticket-badge">{t["number"]}</span>', unsafe_allow_html=True
            )
            st.caption(f"{t['title']}")
            st.caption(f"Priority: {t['priority']} · SLA: {t['sla_target']}")
    else:
        st.caption("No tickets created yet.")

    # Escalations
    if st.session_state.last_escalation:
        st.divider()
        esc = st.session_state.last_escalation
        st.markdown(
            f'<span class="escalation-badge">🚨 {esc["escalation_id"]}</span>',
            unsafe_allow_html=True,
        )
        st.caption(f"Severity: {esc['severity']}")
        st.caption(f"ETA: {esc['estimated_response']}")
        st.caption(f"Contact: {esc['contact_channel']}")

    st.divider()
    if st.button("🗑️ Clear chat", use_container_width=True):
        for key in ["messages", "last_kb_articles", "tickets", "last_escalation", "last_tools_used"]:
            st.session_state[key] = [] if key != "last_escalation" else None
            if key == "last_tools_used":
                st.session_state[key] = []
        st.rerun()


# ──────────────────────────────────────────────
# Main area
# ──────────────────────────────────────────────

st.markdown(
    """
    <div class="agent-header">
        <h1>🤖 IT Support Agent</h1>
        <p>Powered by Claude (Anthropic) · RAG · ServiceNow integration · 
        Portfolio project — Joseph Formica</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Starter prompts (shown when chat is empty)
if not st.session_state.messages:
    st.markdown("**Try asking about:**")
    cols = st.columns(2)
    starters = [
        "I forgot my password and can't log in",
        "How do I set up MFA on my phone?",
        "My VPN keeps disconnecting",
        "I think I was phished — I clicked a suspicious link",
    ]
    for i, starter in enumerate(starters):
        if cols[i % 2].button(f'💬 "{starter}"', key=f"starter_{i}", use_container_width=True):
            st.session_state.starter_prompt = starter
            st.rerun()

# Render conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Handle starter prompt if one was clicked
if hasattr(st.session_state, "starter_prompt"):
    prompt = st.session_state.starter_prompt
    del st.session_state.starter_prompt
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base and reasoning…"):
            result = agent.chat(prompt, st.session_state.messages[:-1])

        response_text = result["response"]
        st.write(response_text)

    st.session_state.messages.append({"role": "assistant", "content": response_text})
    st.session_state.last_kb_articles = result.get("kb_articles", [])
    st.session_state.last_tools_used = result.get("tools_used", [])
    if result.get("ticket"):
        st.session_state.tickets.append(result["ticket"])
    if result.get("escalation"):
        st.session_state.last_escalation = result["escalation"]

    st.rerun()

# Chat input
if prompt := st.chat_input("Describe your IT issue…"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base and reasoning…"):
            result = agent.chat(prompt, st.session_state.messages[:-1])

        response_text = result["response"]
        st.write(response_text)

    st.session_state.messages.append({"role": "assistant", "content": response_text})
    st.session_state.last_kb_articles = result.get("kb_articles", [])
    st.session_state.last_tools_used = result.get("tools_used", [])
    if result.get("ticket"):
        st.session_state.tickets.append(result["ticket"])
    if result.get("escalation"):
        st.session_state.last_escalation = result["escalation"]

    st.rerun()
