import streamlit as st
import pandas as pd
from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpInteger, value

st.set_page_config(page_title="💃 Options Optimizer", layout="centered")

st.title("💃 Options Optimizer")
st.caption("Maximize your premium potential while walking like the boss you are 👑")

# Step 1: Upload or use default
st.subheader("📤 Step 1: Upload CSV or Use Template")

uploaded_file = st.file_uploader("Upload a CSV (columns: Stock, Collateral, Premium)", type=["csv"])

# Load uploaded file or default data
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully! Edit your table below 👇")
    except Exception as e:
        st.error(f"❌ Couldn't read file: {e}")
        df = pd.DataFrame(columns=["Stock", "Collateral", "Premium"])
else:
    st.info("ℹ️ No file uploaded. You can edit this default table or upload your own.")
    df = pd.DataFrame({
        "Stock": ["TTD", "RIVN", "SOFI"],
        "Collateral": [7000, 1500, 1250],
        "Premium": [150, 40, 30]
    })

# Show editable table
st.subheader("✏️ Step 1.5: Edit Your Options Table")
df = st.data_editor(df, num_rows="dynamic", use_container_width=True)


# Step 2: Set Collateral Limit
st.subheader("💰 Step 2: Set Your Collateral Limit")
collateral_limit = st.number_input("Total Available Collateral", value=10430, step=100)

# Step 3: Optimize
if st.button("🚀 Step 3: Optimize!"):
    try:
        df = df[~pd.isna(df["Collateral"])]
        stocks = df["Stock"].tolist()
        collateral = df["Collateral"].tolist()
        premium = df["Premium"].tolist()

        model = LpProblem("Maximize_Premium", LpMaximize)
        x_vars = [LpVariable(f"x_{stock}", lowBound=0, cat=LpInteger) for stock in stocks]

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
            st.success(f"🎯 **Total Premium:** ${total_premium}")
            st.success(f"💅 **Collateral Used:** ${total_collateral}")
            st.dataframe(pd.DataFrame(selected), use_container_width=True)
        else:
            st.warning("⚠️ No contracts fit within your collateral limit. Try adjusting your values.")

    except Exception as e:
        st.error(f"❌ Optimization failed: {e}")