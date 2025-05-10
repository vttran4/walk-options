import streamlit as st
import pandas as pd
from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpInteger, value

st.set_page_config(page_title="🤑 Options Optimizer", layout="centered")

st.title("📈 Hot Girl Options Optimizer")
st.caption("Find the best combo and how many contracts to sell to max your premiums 💅")

# Editable table
st.subheader("🔢 Input Stock Data")
df = st.data_editor(
    pd.DataFrame({
        "Stock": ["TTD", "RIVN", "SOFI"],
        "Collateral": [7000, 1500, 1250],
        "Premium": [150, 34, 16]
    }),
    num_rows="dynamic",
    use_container_width=True
)

# Collateral Limit Input
collateral_limit = st.number_input("💰 Total Collateral Limit", value=10430, step=100)

if st.button("🔥 Optimize!"):
    stocks = df["Stock"].tolist()
    collateral = df["Collateral"].tolist()
    premium = df["Premium"].tolist()

    # Set up LP problem
    model = LpProblem("Maximize_Premium", LpMaximize)
    x_vars = [LpVariable(f"x_{stock}", lowBound=0, cat=LpInteger) for stock in stocks]

    # Objective: Maximize premium
    model += lpSum([x_vars[i] * premium[i] for i in range(len(stocks))]), "Total_Premium"

    # Constraint: Total collateral ≤ limit
    model += lpSum([x_vars[i] * collateral[i] for i in range(len(stocks))]) <= collateral_limit, "Collateral_Limit"

    # Solve it
    model.solve()

    selected = []
    total_premium = 0
    total_collateral = 0

    for i, stock in enumerate(stocks):
        qty = int(value(x_vars[i]))
        if qty > 0:
            total_premium += premium[i] * qty
            total_collateral += collateral[i] * qty
            selected.append({
                "Stock": stock,
                "Contracts": qty,
                "Collateral per": collateral[i],
                "Premium per": premium[i],
                "Total Premium": premium[i] * qty,
                "Total Collateral": collateral[i] * qty
            })

    st.success(f"✅ Total Premium: ${total_premium} | 🔒 Collateral Used: ${total_collateral}")
    st.dataframe(pd.DataFrame(selected))