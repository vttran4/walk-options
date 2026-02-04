from __future__ import annotations

from dataclasses import dataclass
from typing import List

import pandas as pd
from pulp import LpInteger, LpMaximize, LpProblem, LpVariable, lpSum, value


@dataclass
class OptimizationResult:
    selected: List[dict]
    total_premium: float
    total_collateral: float


def optimize_options(df: pd.DataFrame, collateral_limit: float) -> OptimizationResult:
    """
    Maximize total premium with integer contract counts under a collateral limit.
    Expects columns: Stock, Collateral, Premium
    """
    stocks = df["Stock"].tolist()
    collateral = df["Collateral"].tolist()
    premium = df["Premium"].tolist()

    model = LpProblem("Maximize_Premium", LpMaximize)
    x_vars = [LpVariable(f"x_{stock}", lowBound=0, cat=LpInteger) for stock in stocks]

    model += lpSum([x_vars[i] * premium[i] for i in range(len(stocks))]), "Total_Premium"
    model += (
        lpSum([x_vars[i] * collateral[i] for i in range(len(stocks))]) <= collateral_limit,
        "Collateral_Limit",
    )
    model.solve()

    selected: List[dict] = []
    total_premium = 0.0
    total_collateral = 0.0

    for i, stock in enumerate(stocks):
        qty = int(value(x_vars[i]))
        if qty > 0:
            total_premium += premium[i] * qty
            total_collateral += collateral[i] * qty
            selected.append(
                {
                    "Stock": stock,
                    "Contracts": qty,
                    "Collateral Each": f"${collateral[i]}",
                    "Premium Each": f"${premium[i]}",
                    "Total Collateral": f"${collateral[i] * qty}",
                    "Total Premium": f"${premium[i] * qty}",
                }
            )

    return OptimizationResult(
        selected=selected,
        total_premium=total_premium,
        total_collateral=total_collateral,
    )
