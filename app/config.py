import os

from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5")

if not ANTHROPIC_API_KEY:
    raise RuntimeError(
        "ANTHROPIC_API_KEY is not set. Copy .env.example to .env and set your API key."
    )

# Optional: only required if you want EmailAgent to actually send mail instead of
# just drafting it. Left unset, EmailAgent still drafts a subject/body but reports
# that it could not send.
SMTP_HOST = os.environ.get("SMTP_HOST", "")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USERNAME = os.environ.get("SMTP_USERNAME", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
SMTP_FROM_EMAIL = os.environ.get("SMTP_FROM_EMAIL", SMTP_USERNAME)
