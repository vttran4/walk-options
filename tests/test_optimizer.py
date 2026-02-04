import pandas as pd

from core.optimizer import optimize_options
from core.validation import validate_inputs


def test_optimize_options_picks_best_premium():
    df = pd.DataFrame(
        {
            "Stock": ["A", "B"],
            "Collateral": [100, 200],
            "Premium": [10, 30],
        }
    )

    result = optimize_options(df, collateral_limit=200)

    assert result.total_premium == 30
    assert result.total_collateral == 200
    assert len(result.selected) == 1
    assert result.selected[0]["Stock"] == "B"


def test_validate_inputs_missing_columns():
    df = pd.DataFrame({"Stock": ["A"], "Collateral": [100]})
    validation = validate_inputs(df)

    assert validation.ok is False
    assert any("Missing columns" in msg for msg in validation.errors)
