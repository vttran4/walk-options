from __future__ import annotations

from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from core.optimizer import optimize_options
from core.validation import validate_inputs

app = FastAPI(title="Options Optimizer API", version="1.0.0")


class OptimizeRequest(BaseModel):
    rows: list[dict[str, Any]] = Field(..., description="Rows with Stock, Collateral, Premium")
    collateral_limit: float = Field(..., ge=0)


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/optimize")
def optimize(req: OptimizeRequest) -> Dict[str, Any]:
    if not req.rows:
        raise HTTPException(status_code=400, detail="No rows provided.")

    df = validate_inputs_from_rows(req.rows)
    validation = validate_inputs(df)
    if not validation.ok:
        raise HTTPException(status_code=400, detail="; ".join(validation.errors))

    result = optimize_options(validation.df, req.collateral_limit)
    return {
        "selected": result.selected,
        "total_premium": result.total_premium,
        "total_collateral": result.total_collateral,
    }


def validate_inputs_from_rows(rows: list[dict[str, Any]]):
    # Keep only expected keys to avoid unexpected payloads
    cleaned_rows = []
    for row in rows:
        cleaned_rows.append(
            {
                "Stock": row.get("Stock"),
                "Collateral": row.get("Collateral"),
                "Premium": row.get("Premium"),
            }
        )
    return __import__("pandas").DataFrame(cleaned_rows)
