import json

from anthropic import Anthropic

from app.agents import email_agent, servicenow_agent, splunk_agent
from app.config import ANTHROPIC_API_KEY, CLAUDE_MODEL

MAX_TURNS = 6

COORDINATOR_SYSTEM_PROMPT = """You are the OPS Coordinator Agent.

Your job:
1. Understand the user request.
2. Decide which sub-agents must be activated.
3. Pass the correct context and data to each sub-agent.
4. Combine all sub-agent outputs into a final response.

Available Sub-Agents (call them as tools):
- servicenow_agent: Fetch and analyze ticket details. Requires a ticket_id (e.g. "INC0012345") \
extracted from the user's request. If no ticket ID is mentioned, make your best guess at \
which ticket is being discussed, or pass an empty string.
- splunk_agent: Run log analysis for a service. Requires a service name (e.g. "payment-service"). \
If the user only gave a ticket ID, first call servicenow_agent to learn the affected_service, \
then call splunk_agent with that service name.
- email_agent: Draft AND actually send a final email report summarizing findings. Requires \
ticket_summary and log_analysis_summary text (use the outputs of the other two agents; if one \
wasn't run, use a short reasonable placeholder). Also pass recipient_email: the exact email \
address the user gave in their request (e.g. "email alice@example.com the report" -> \
"alice@example.com"). If the user did not give an email address, pass an empty string for \
recipient_email — the email will still be drafted but not sent.

Routing Rules:
- If user asks for "ticket analysis", "incident analysis", "log analysis", "root cause", "SLA", \
"error details", or mentions a ticket ID -> activate servicenow_agent + splunk_agent + email_agent.
- If user only asks for logs -> activate splunk_agent only.
- If user asks to send or prepare a report -> activate email_agent (plus whichever other agents \
are needed to gather the content it summarizes).

Once you have gathered everything you need from the sub-agents you activated, respond with a \
FINAL message containing ONLY strict JSON (no markdown, no commentary) in exactly this shape:
{
  "ticket_summary": "<result from servicenow_agent, or 'Not requested.' if it wasn't activated>",
  "log_analysis_summary": "<result from splunk_agent, or 'Not requested.' if it wasn't activated>",
  "recommended_fix": "<your own recommended fix synthesized from the above>",
  "email_report": <the exact JSON object returned by the email_agent tool_result, unmodified> or \
{"subject": "Not requested.", "body": "Not requested.", "recipient": "", "sent": false, "error": null} \
if email_agent wasn't activated
}
"""

TOOLS = [
    {
        "name": "servicenow_agent",
        "description": "Fetch and analyze ServiceNow ticket details for a given ticket ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "ticket_id": {"type": "string", "description": "The ServiceNow ticket ID, e.g. INC0012345"},
            },
            "required": ["ticket_id"],
        },
    },
    {
        "name": "splunk_agent",
        "description": "Run Splunk log analysis for a given service name.",
        "input_schema": {
            "type": "object",
            "properties": {
                "service": {"type": "string", "description": "The affected service name, e.g. payment-service"},
            },
            "required": ["service"],
        },
    },
    {
        "name": "email_agent",
        "description": "Draft and send a final email report summarizing ticket and log analysis findings.",
        "input_schema": {
            "type": "object",
            "properties": {
                "ticket_summary": {"type": "string", "description": "Summary from servicenow_agent"},
                "log_analysis_summary": {"type": "string", "description": "Summary from splunk_agent"},
                "recipient_email": {
                    "type": "string",
                    "description": "Email address to send the report to, exactly as given by the user. Empty string if none was given.",
                },
            },
            "required": ["ticket_summary", "log_analysis_summary", "recipient_email"],
        },
    },
]

_client = Anthropic(api_key=ANTHROPIC_API_KEY)


def _dispatch_tool(name: str, tool_input: dict) -> str:
    if name == "servicenow_agent":
        return servicenow_agent.run(_client, tool_input.get("ticket_id", ""))
    if name == "splunk_agent":
        return splunk_agent.run(_client, tool_input.get("service", ""))
    if name == "email_agent":
        result = email_agent.run(
            _client,
            tool_input.get("ticket_summary", ""),
            tool_input.get("log_analysis_summary", ""),
            tool_input.get("recipient_email", ""),
        )
        return json.dumps(result)
    return f"Unknown tool: {name}"


def _fallback_response(raw_text: str) -> dict:
    return {
        "ticket_summary": raw_text,
        "log_analysis_summary": "Not available (coordinator did not return structured JSON).",
        "recommended_fix": "Not available (coordinator did not return structured JSON).",
        "email_report": {
            "subject": "Incident Report",
            "body": raw_text,
            "recipient": "",
            "sent": False,
            "error": None,
        },
    }


def handle_request(user_request: str) -> dict:
    messages = [{"role": "user", "content": user_request}]

    for _ in range(MAX_TURNS):
        response = _client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1500,
            system=COORDINATOR_SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            final_text = "".join(
                block.text for block in response.content if block.type == "text"
            ).strip()
            try:
                return json.loads(final_text)
            except ValueError:
                return _fallback_response(final_text)

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result_text = _dispatch_tool(block.name, block.input)
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result_text,
                    }
                )
        messages.append({"role": "user", "content": tool_results})

    return _fallback_response(
        "The coordinator did not reach a final answer within the allowed number of turns."
    )
