import json

from anthropic import Anthropic

from app.config import CLAUDE_MODEL
from data.dummy_data import get_ticket

SYSTEM_PROMPT = """You are ServiceNowAgent, a specialist sub-agent in an IT operations \
support system. You are given the raw JSON record for a single ServiceNow ticket. \
Produce a concise ticket analysis covering: what the issue is, its priority, its SLA \
status, and the affected service. Write plain text (no JSON, no markdown headers), \
3-5 sentences."""


def run(client: Anthropic, ticket_id: str) -> str:
    ticket = get_ticket(ticket_id)

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Ticket record:\n{json.dumps(ticket, indent=2)}",
            }
        ],
    )
    return response.content[0].text
