# IT Support Agent — AI Portfolio Project

**Built by Joseph Formica** · [LinkedIn](https://linkedin.com/in/josephformica)

An end-to-end agentic RAG system that automates IT helpdesk triage. The agent searches a knowledge base, drafts step-by-step resolutions, creates ServiceNow tickets, and escalates critical incidents — all driven by natural language.

> **Live demo:** [Hugging Face Spaces link] &nbsp;|&nbsp; **Stack:** Python · Anthropic API · ChromaDB · sentence-transformers · Streamlit

---

## Why I Built This

In my role at ZOLL Medical, I built a Microsoft Copilot Studio agent that handles IT support triage. This project is a from-scratch reimplementation in pure Python — bypassing the low-code layer to work directly with LLM APIs, vector databases, and the tool-use agentic pattern. The goal was to prove I understand *how* these systems work, not just how to configure them.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Streamlit UI                        │
│         Chat interface · KB sidebar · Ticket panel      │
└──────────────────────┬──────────────────────────────────┘
                       │ user message + conversation history
                       ▼
┌─────────────────────────────────────────────────────────┐
│                  IT Support Agent                       │
│              agent.py — agentic loop                    │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │          Claude (claude-sonnet-4-6)              │   │
│  │     Tool use · Grounded response generation      │   │
│  └────────┬──────────────┬──────────────┬───────────┘   │
│           │              │              │                │
│  search_kb│   create_    │  escalate_   │                │
│           │   ticket     │  to_human    │                │
│           ▼              ▼              ▼                │
│  ┌─────────────┐  ┌──────────────┐ ┌──────────────┐     │
│  │ RAG Layer   │  │  ServiceNow  │ │  Escalation  │     │
│  │  rag.py     │  │  tools.py    │ │  tools.py    │     │
│  └──────┬──────┘  └──────────────┘ └──────────────┘     │
│         │                                               │
│         ▼                                               │
│  ┌─────────────────────────────────────────────────┐    │
│  │  ChromaDB (cosine similarity search)            │    │
│  │  sentence-transformers: all-MiniLM-L6-v2        │    │
│  │  10 KB articles · chunked · embedded locally    │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

## How the Agentic Loop Works

1. **User sends a message** — the Streamlit UI passes it to `ITSupportAgent.chat()` along with the conversation history
2. **Claude reasons and selects tools** — the system prompt instructs it to always search the KB first
3. **Tool execution** — `_run_tool()` dispatches to the appropriate function and returns results as a tool_result message
4. **Continuation** — tool results are appended to messages and Claude is called again; this loops until `stop_reason == "end_turn"`
5. **Grounded response** — the final response cites retrieved KB content and summarises any actions taken (ticket number, escalation ID)

Claude can call multiple tools per turn (e.g., KB search → ticket creation) in a single agentic pass.

---

## Tech Stack

| Layer | Technology | Why |
|---|---|---|
| LLM | Anthropic API (`claude-sonnet-4-6`) | Best-in-class tool use; reliable agentic behaviour |
| Embeddings | `sentence-transformers` (`all-MiniLM-L6-v2`) | Free, local, no embedding API cost |
| Vector DB | ChromaDB (persistent) | Zero infrastructure; production-ready API |
| UI | Streamlit | Fast to ship; lets the agent be the demo, not the framework |
| Env | `python-dotenv` | Standard secret management |

---

## Project Structure

```
it-support-agent/
├── app.py              # Streamlit chat UI
├── agent.py            # Agentic loop + tool dispatch
├── rag.py              # ChromaDB semantic search
├── tools.py            # Tool implementations (ServiceNow, escalation)
├── ingest.py           # One-time KB ingestion script
├── requirements.txt
├── .env.example
├── kb/                 # 10 IT knowledge base articles (Markdown)
│   ├── 01_password_reset_entra.md
│   ├── 02_mfa_setup.md
│   └── ...
└── evals/
    ├── test_cases.json     # 20 labelled test cases
    └── run_evals.py        # Harness with LLM-as-judge scoring
```

---

## Setup

### 1. Clone and install
```bash
git clone https://github.com/yourusername/it-support-agent
cd it-support-agent
pip install -r requirements.txt
```

### 2. Add your API key
```bash
cp .env.example .env
# Edit .env and add your Anthropic API key
# Get one at: https://console.anthropic.com
```

### 3. Ingest the knowledge base
```bash
python ingest.py
```
This downloads the sentence-transformers model (~80 MB, first run only), chunks the KB articles, and stores embeddings in `./chroma_db/`.

### 4. Run the app
```bash
streamlit run app.py
```
Open http://localhost:8501 in your browser.

### 5. Run evaluations (optional)
```bash
python evals/run_evals.py
```

---

## Eval Results

The evaluation harness runs 20 test cases covering easy, medium, and hard scenarios across 5 categories. Claude is scored on tool accuracy, ticket/escalation decision accuracy, and response quality (LLM-as-judge using Claude Haiku).

| Metric | Score |
|---|---|
| Tool accuracy | Run `evals/run_evals.py` to generate |
| Ticket accuracy | — |
| Escalation accuracy | — |
| Avg quality (LLM judge) | — |

> Run the eval script and paste your results here.

---

## What I'd Improve Next

- **Streaming responses** — use `client.messages.stream()` for real-time text output
- **Persistent conversation memory** — store full tool-use message history in session state for tighter multi-turn follow-up
- **Azure OpenAI + Azure AI Search** — swap in Azure-native services to target Microsoft-ecosystem SE roles
- **Actual ServiceNow API** — replace mock tool with real ServiceNow REST calls
- **Retrieval eval with RAGAS** — automated retrieval precision/recall scoring beyond LLM-as-judge
- **Feedback loop** — thumbs up/down in UI feeds back to improve chunking/retrieval

---

## Background

This project demonstrates competencies relevant to AI Solutions Engineer roles:
- **Agentic system design** — multi-tool orchestration with a real reasoning loop
- **RAG pipeline** — chunking, embedding, vector search, retrieval grounding
- **LLM API fluency** — direct Anthropic SDK usage, tool use schema design, message history management
- **Evaluation** — structured test cases + LLM-as-judge pattern
- **Technical communication** — this README, written as a solution architecture doc

Built on top of my work at ZOLL Medical Corporation, where I built production AI agents using Microsoft Copilot Studio for the same IT support use case.
