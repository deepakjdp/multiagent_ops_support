# OPS Support Coordinator — Demo Guide

A live walkthrough script for demoing the multi-agent IT ops assistant: a Claude-powered
**OPS Coordinator** that routes free-text requests to three sub-agents — **ServiceNowAgent**,
**SplunkAgent**, and **EmailAgent** — via Claude's tool-use (function calling), and replies
through a chatbot UI.

> For full technical documentation (architecture diagrams, every endpoint, file reference),
> see [`README.md`](./README.md). This file is just the demo script.

---

## 1. What you're demoing

| | |
|---|---|
| **Coordinator** | Claude decides which sub-agents to call, based on routing rules in its own system prompt — no hardcoded if/else routing in Python. |
| **ServiceNowAgent** | Looks up a ticket and asks Claude to summarize priority, SLA status, and affected service. |
| **SplunkAgent** | Looks up logs for a service and asks Claude for an error pattern + root-cause hypothesis. |
| **EmailAgent** | Drafts a subject/body with Claude, then **actually sends it via SMTP** if the user gave a recipient email address. |
| **One real AI dependency** | All four calls above hit the same Claude API (`claude-sonnet-5`) — each sub-agent is a plain Python function with its own prompt, not a separate system. |
| **Frontend** | A chatbot UI (not a form) — type a request, get a reply, with example-prompt buttons for a fast demo. |

---

## 2. Before the demo (one-time setup)

- [ ] `pip install -r requirements.txt`
- [ ] `cp .env.example .env`
- [ ] Add a real `ANTHROPIC_API_KEY` to `.env` (with billing/credit on the account — see
      [console.anthropic.com](https://console.anthropic.com))
- [ ] *(Optional, for the "real email send" moment)* Add SMTP credentials to `.env`. For a
      safe demo that doesn't spam anyone, use [Ethereal Email](https://ethereal.email/create)
      — it generates throwaway SMTP credentials instantly and catches mail in a fake inbox
      instead of delivering it.
- [ ] Start the server: `uvicorn app.main:app --reload`
- [ ] Open **http://localhost:8000/** in a browser and confirm the chat UI loads

---

## 3. Demo script

Run these in order. Each one highlights a different part of the system.

### Step 1 — Full analysis (all three agents)

> **Type:** `Do a root cause analysis on ticket INC0012345 and email me the report`

**What to point out:**
- The routing rule fires because the message contains "root cause" + a ticket ID →
  `ServiceNowAgent`, `SplunkAgent`, and `EmailAgent` all activate in one request.
- The reply comes back as three readable sections (Ticket Summary, Log Analysis,
  Recommended Fix) plus a drafted Email Report — all from one chat message.
- `INC0012345` is a payment-service outage (intermittent 500s after a deploy) — the log
  summary should mention the downstream fraud-check timeout pattern.

### Step 2 — Logs only (single agent)

> **Type:** `Just show me the splunk logs for search-service`

**What to point out:**
- Only `SplunkAgent` runs this time — Ticket Summary and Recommended Fix come back as
  "Not requested." This is the coordinator making a routing decision, not a fixed pipeline.
- `search-service` logs show Elasticsearch shard allocation failures / query timeouts.

### Step 3 — Email with a real recipient (send, not just draft)

> **Type:** `Send the incident report for INC0012345 to <your-test-inbox>`

**What to point out:**
- `EmailAgent` drafts the email with Claude, then calls SMTP to actually send it — the
  reply bubble shows a status line: **"✓ Sent to ‹address›"**.
- If no address is given, or SMTP isn't configured, it still drafts the email but shows
  **"✗ Drafted only — no recipient email address was given"** instead of silently failing.
- If using Ethereal, open the Ethereal inbox link to show the real email that arrived.

### Step 4 — An unknown ticket (graceful fallback)

> **Type:** `What's the status of ticket INC9999999?`

**What to point out:**
- No crash, no 500 error — `data/dummy_data.py` returns a generic "no matching ticket
  found" record, and the coordinator reports that cleanly instead of failing.

### Step 5 (optional) — Show the architecture

Open the published architecture diagram (or the Mermaid diagram in `README.md`) and walk
through: Client → FastAPI → Coordinator (tool-use loop) → three sub-agents → one shared
Claude API, called independently up to four times per request.

---

## 4. Sample data reference

Use any of these ticket IDs / service names during the demo:

| Ticket ID | Service | Scenario |
|---|---|---|
| `INC0012345` | payment-service | Intermittent 500s after a deploy (fraud-check timeout) |
| `INC0012678` | auth-service | SSO login failures (JWT signature errors) |
| `INC0013002` | order-service | Order history page loading slowly |
| `INC0013450` | notification-service | Push notifications delayed 20+ min |
| `INC0013789` | inventory-service | Stock counts not syncing (warehouse API 429s) |
| `INC0014021` | search-service | Zero search results (Elasticsearch shard failures) |
| `INC0014205` | shipping-service | International shipping labels failing |
| `INC0014502` | checkout-service | Cart emptied after applying a promo code |

---

## 5. If something goes wrong mid-demo

| Symptom | Likely cause | Fix |
|---|---|---|
| `500` error, "ANTHROPIC_API_KEY is not set" | `.env` missing or key not loaded | Confirm `.env` exists next to `app/`, restart the server |
| `400` error, "credit balance is too low" | Anthropic account has no billing/credit | Add a payment method at console.anthropic.com |
| Email always shows "Drafted only" | No recipient email in the message, or SMTP unset | Include an explicit email address in the request; check `SMTP_HOST`/`SMTP_USERNAME`/`SMTP_PASSWORD` in `.env` |
| Chat hangs for a long time | Normal — a full analysis makes 3-4 sequential Claude calls | Mention this while waiting; it's the tool-use loop working, not a freeze |
| Port 8000 won't bind (Windows) | Port reserved by Windows | Run on another port: `uvicorn app.main:app --port 8010` |

---

## 6. Response shape (for a technical audience)

```json
{
  "ticket_summary": "...",
  "log_analysis_summary": "...",
  "recommended_fix": "...",
  "email_report": {
    "subject": "...",
    "body": "...",
    "recipient": "...",
    "sent": true,
    "error": null
  }
}
```
