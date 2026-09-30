"""FastAPI service and same-origin host for the static dashboard."""

from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from backend.inference import AspectSentimentModel


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL: AspectSentimentModel | None = None
MODEL_ERROR: str | None = None


@asynccontextmanager
async def lifespan(_: FastAPI):
    global MODEL, MODEL_ERROR
    try:
        MODEL = AspectSentimentModel()
        MODEL_ERROR = None
        print(
            "Loaded",
            MODEL.manifest.get("model_name", "aspect sentiment model"),
            "from",
            MODEL.model_dir,
        )
    except Exception as exc:  # Keep the dashboard available while a checkpoint is absent.
        MODEL = None
        MODEL_ERROR = str(exc)
        print(f"Inference model unavailable: {MODEL_ERROR}")
    yield


app = FastAPI(
    title="Hinglish E-commerce ABSA API",
    version="1.0.0",
    description="Aspect sentiment inference using the checkpoint exported by notebook 06.",
    lifespan=lifespan,
)


class AnalyzeRequest(BaseModel):
    reviews: list[str] = Field(min_length=1, max_length=100)


@app.get("/api/health")
def health() -> dict[str, Any]:
    return {
        "ready": MODEL is not None,
        "model": MODEL.manifest.get("model_name") if MODEL else None,
        "device": str(MODEL.device) if MODEL else None,
        "error": None if MODEL else "Trained checkpoint unavailable or failed to load.",
    }


@app.post("/api/analyze")
def analyze(payload: AnalyzeRequest) -> dict[str, Any]:
    if MODEL is None:
        raise HTTPException(
            status_code=503,
            detail="The trained model checkpoint is not installed. See backend/README.md.",
        )
    if any(not review.strip() for review in payload.reviews):
        raise HTTPException(status_code=422, detail="Reviews must not be empty.")
    if any(len(review) > 5000 for review in payload.reviews):
        raise HTTPException(status_code=413, detail="Each review must be 5,000 characters or fewer.")

    results = MODEL.predict([review.strip() for review in payload.reviews])
    return {
        "model": MODEL.manifest.get("model_name", "Trained model"),
        "model_seed": MODEL.manifest.get("seed"),
        "source": "fine-tuned checkpoint",
        "results": results,
    }


@app.get("/", include_in_schema=False)
def dashboard() -> FileResponse:
    index = PROJECT_ROOT / "dashboard" / "index.html"
    if not index.is_file():
        raise HTTPException(status_code=404, detail="Dashboard file is missing.")
    return FileResponse(index)
