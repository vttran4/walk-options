import os

import pandas as pd
import requests
import streamlit as st

from core.validation import validate_inputs

st.set_page_config(page_title="💃 Options Optimizer", layout="centered")

st.title("💃 Options Optimizer")
st.caption("Maximize your premium potential while walking 🎀")

# Step 1: Upload or use default
st.subheader("📤 Step 1: Upload XLSX or Use Template")

uploaded_file = st.file_uploader("Upload an Excel file (.xlsx) with columns: Stock, Collateral, Premium", type=["xlsx"])

# Load uploaded file or default data
if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, engine = "openpyxl")
        st.success("✅ File uploaded successfully! Edit your table below 👇")
    except Exception as e:
        st.error(f"❌ Couldn't read Excel file: {e}")
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

# API endpoint (Phase 2)
api_base_url = os.environ.get("OPTIMIZER_API_URL", "http://127.0.0.1:8000")

# Step 3: Optimize
if st.button("🚀 Step 3: Optimize!"):
    try:
        validation = validate_inputs(df)
        if not validation.ok:
            for msg in validation.errors:
                st.error(f"❌ {msg}")
        else:
            payload = {
                "rows": validation.df.to_dict(orient="records"),
                "collateral_limit": collateral_limit,
            }
            resp = requests.post(f"{api_base_url}/optimize", json=payload, timeout=20)
            if resp.status_code != 200:
                st.error(f"❌ API error: {resp.text}")
            else:
                data = resp.json()
                if data.get("selected"):
                    st.success(f"🎯 **Total Premium:** ${data['total_premium']}")
                    st.success(f"💅 **Collateral Used:** ${data['total_collateral']}")
                    st.dataframe(pd.DataFrame(data["selected"]), use_container_width=True)
                else:
                    st.warning(
                        "⚠️ No contracts fit within your collateral limit. Try adjusting your values."
                    )

    except Exception as e:
        st.error(f"❌ Optimization failed: {e}")
