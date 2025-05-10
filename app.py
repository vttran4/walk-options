import streamlit as st
import pandas as pd
from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpBinary, value

st.set_page_config(page_title="🤑 Options Optimizer", layout="centered")

st.title("📈 Hot Girl Options Optimizer")
st.caption("Pick the best combo of contracts to sell based on your premium goals 💅")

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

    # Set up the LP problem
    model = LpProblem("Maximize_Premium", LpMaximize)
    x_vars = [LpVariable(f"x_{stock}", cat=LpBinary) for stock in stocks]

    # Objective: Maximize total premium
    model += lpSum([x_vars[i] * premium[i] for i in range(len(stocks))]), "Total_Premium"

    # Constraint: Total collateral ≤ limit
    model += lpSum([x_vars[i] * collateral[i] for i in range(len(stocks))]) <= collateral_limit, "Collateral_Limit"

    # Solve it
    model.solve()

    selected = []
    total_premium = 0
    total_collateral = 0

    for i, stock in enumerate(stocks):
        if value(x_vars[i]) == 1:
            selected.append({
                "Stock": stock,
                "Collateral": collateral[i],
                "Premium": premium[i]
            })
            total_premium += premium[i]
            total_collateral += collateral[i]

    st.success(f"✅ Total Premium: ${total_premium} | 🔒 Collateral Used: ${total_collateral}")
    st.dataframe(pd.DataFrame(selected))