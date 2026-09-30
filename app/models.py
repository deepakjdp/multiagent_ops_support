from typing import Optional

from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    request: str


class EmailReport(BaseModel):
    subject: str
    body: str
    recipient: str = ""
    sent: bool = False
    error: Optional[str] = None


class AnalysisResponse(BaseModel):
    ticket_summary: str
    log_analysis_summary: str
    recommended_fix: str
    email_report: EmailReport
