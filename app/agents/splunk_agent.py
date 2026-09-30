import json

from anthropic import Anthropic

from app.config import CLAUDE_MODEL
from data.dummy_data import get_logs

SYSTEM_PROMPT = """You are SplunkAgent, a specialist sub-agent in an IT operations \
support system. You are given a batch of raw log entries for a service. Analyze them \
for error patterns, frequency, and a likely root cause hypothesis. Write plain text \
(no JSON, no markdown headers), 3-5 sentences."""


def run(client: Anthropic, service: str) -> str:
    logs = get_logs(service)

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Service: {service}\nLog entries:\n{json.dumps(logs, indent=2)}",
            }
        ],
    )
    return response.content[0].text
