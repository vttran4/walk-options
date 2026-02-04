from __future__ import annotations

from dataclasses import dataclass
from typing import List

import pandas as pd


REQUIRED_COLUMNS = ["Stock", "Collateral", "Premium"]


@dataclass
class ValidationResult:
    ok: bool
    errors: List[str]
    df: pd.DataFrame


def validate_inputs(df: pd.DataFrame) -> ValidationResult:
    errors: List[str] = []

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        errors.append(f"Missing columns: {', '.join(missing)}")
        return ValidationResult(ok=False, errors=errors, df=df)

    cleaned = df.copy()

    # Drop completely empty rows
    cleaned = cleaned.dropna(how="all")

    # Coerce numeric columns
    for col in ["Collateral", "Premium"]:
        cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")

    # Basic checks
    if cleaned["Stock"].isna().any():
        errors.append("Stock column has empty values.")

    if cleaned[["Collateral", "Premium"]].isna().any().any():
        errors.append("Collateral or Premium has non-numeric or empty values.")

    if (cleaned[["Collateral", "Premium"]] < 0).any().any():
        errors.append("Collateral and Premium must be non-negative.")

    return ValidationResult(ok=len(errors) == 0, errors=errors, df=cleaned)
