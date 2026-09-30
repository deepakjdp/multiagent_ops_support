from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from app import coordinator
from app.models import AnalysisResponse, AnalyzeRequest

app = FastAPI(title="OPS Coordinator Multi-Agent System")

STATIC_DIR = Path(__file__).parent / "static"


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/analyze", response_model=AnalysisResponse)
def analyze(payload: AnalyzeRequest) -> AnalysisResponse:
    try:
        result = coordinator.handle_request(payload.request)
        return AnalysisResponse(**result)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
