import json
import smtplib
from email.mime.text import MIMEText

from anthropic import Anthropic

from app.config import (
    CLAUDE_MODEL,
    SMTP_FROM_EMAIL,
    SMTP_HOST,
    SMTP_PASSWORD,
    SMTP_PORT,
    SMTP_USERNAME,
)

SYSTEM_PROMPT = """You are EmailAgent, a specialist sub-agent in an IT operations \
support system. Given a ticket summary and a log analysis summary, draft a concise, \
professional incident report email. Respond with strict JSON only, no markdown, in \
exactly this shape: {"subject": "...", "body": "..."}"""


def _draft(client: Anthropic, ticket_summary: str, log_analysis_summary: str) -> dict:
    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=600,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Ticket summary:\n{ticket_summary}\n\n"
                    f"Log analysis summary:\n{log_analysis_summary}"
                ),
            }
        ],
    )
    text = response.content[0].text.strip()
    try:
        return json.loads(text)
    except ValueError:
        return {"subject": "Incident Report", "body": text}


def _send(recipient: str, subject: str, body: str) -> dict:
    if not SMTP_HOST or not SMTP_USERNAME or not SMTP_PASSWORD:
        return {
            "sent": False,
            "error": "SMTP is not configured (set SMTP_HOST, SMTP_USERNAME, and SMTP_PASSWORD in .env).",
        }

    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = SMTP_FROM_EMAIL or SMTP_USERNAME
    message["To"] = recipient

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_FROM_EMAIL or SMTP_USERNAME, [recipient], message.as_string())
        return {"sent": True, "error": None}
    except Exception as exc:  # noqa: BLE001
        return {"sent": False, "error": str(exc)}


def run(
    client: Anthropic,
    ticket_summary: str,
    log_analysis_summary: str,
    recipient: str = "",
) -> dict:
    draft = _draft(client, ticket_summary, log_analysis_summary)
    result = {
        "subject": draft.get("subject", "Incident Report"),
        "body": draft.get("body", ""),
        "recipient": recipient,
        "sent": False,
        "error": None,
    }

    if recipient:
        result.update(_send(recipient, result["subject"], result["body"]))
    else:
        result["error"] = "No recipient email address was found in the request, so the email was only drafted, not sent."

    return result
