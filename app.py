import streamlit as st
import pandas as pd
from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpInteger, value

# Mobile-friendly layout
st.set_page_config(page_title="📱 Hot Girl Options Optimizer", layout="centered")

# Title section
st.title("💅 Hot Girl Options Optimizer")
st.caption("Maximize your premium potential while walking like the boss you are 👑")

# Editable table
st.subheader("📊 Step 1: Enter Your Stock Data")
df = st.data_editor(
    pd.DataFrame({
        "Stock": ["TTD", "RIVN", "SOFI"],
        "Collateral": [7000, 1500, 1250],
        "Premium": [150, 40, 30]
    }),
    num_rows="dynamic",
    use_container_width=True
)

# Collateral input
st.subheader("💰 Step 2: Set Your Collateral Limit")
collateral_limit = st.number_input("Total Available Collateral", value=10430, step=100)

# Optimization logic
if st.button("🚀 Step 3: Optimize!"):
    stocks = df["Stock"].tolist()
    collateral = df["Collateral"].tolist()
    premium = df["Premium"].tolist()

    model = LpProblem("Maximize_Premium", LpMaximize)
    x_vars = [LpVariable(f"x_{stock}", lowBound=0, cat=LpInteger) for stock in stocks]

    # Maximize total premium
    model += lpSum([x_vars[i] * premium[i] for i in range(len(stocks))]), "Total_Premium"
    model += lpSum([x_vars[i] * collateral[i] for i in range(len(stocks))]) <= collateral_limit, "Collateral_Limit"
    model.solve()

    # Results
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
                "Collateral Each": f"${collateral[i]}",
                "Premium Each": f"${premium[i]}",
                "Total Collateral": f"${collateral[i] * qty}",
                "Total Premium": f"${premium[i] * qty}"
            })

    if selected:
        st.success(f"""🎯 **Total Premium:** ${total_premium}
         🔒 **Collateral Used:** ${total_collateral}""")
        
        st.dataframe(pd.DataFrame(selected), use_container_width=True)
    else:
        st.warning("⚠️ No contracts fit within your collateral limit. Try adjusting your values.")