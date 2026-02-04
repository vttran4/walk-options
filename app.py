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


def call_optimize_api(rows, limit):
    payload = {"rows": rows, "collateral_limit": limit}
    resp = requests.post(f"{api_base_url}/optimize", json=payload, timeout=20)
    if resp.status_code != 200:
        raise RuntimeError(resp.text)
    return resp.json()

# Step 3: Optimize
if st.button("🚀 Step 3: Optimize!"):
    try:
        validation = validate_inputs(df)
        if not validation.ok:
            for msg in validation.errors:
                st.error(f"❌ {msg}")
        else:
            rows = validation.df.to_dict(orient="records")
            data = call_optimize_api(rows, collateral_limit)

            if data.get("selected"):
                st.success(f"🎯 **Total Premium:** ${data['total_premium']}")
                st.success(f"💅 **Collateral Used:** ${data['total_collateral']}")
                st.dataframe(pd.DataFrame(data["selected"]), use_container_width=True)
            else:
                st.warning(
                    "⚠️ No contracts fit within your collateral limit. Try adjusting your values."
                )

            # Phase 3: Scenario Analysis
            st.subheader("📈 Phase 3: Scenario Analysis")
            run_scenarios = st.checkbox("Compare ±10% and ±20% scenarios", value=True)
            if run_scenarios:
                scenario_map = {
                    "-20% Premium": (0.8, 1.0),
                    "-10% Premium": (0.9, 1.0),
                    "Base": (1.0, 1.0),
                    "+10% Premium": (1.1, 1.0),
                    "+20% Premium": (1.2, 1.0),
                }
                results = []
                for label, (premium_mult, collateral_mult) in scenario_map.items():
                    scenario_rows = []
                    for row in rows:
                        scenario_rows.append(
                            {
                                "Stock": row["Stock"],
                                "Collateral": row["Collateral"] * collateral_mult,
                                "Premium": row["Premium"] * premium_mult,
                            }
                        )
                    scenario_data = call_optimize_api(scenario_rows, collateral_limit)
                    results.append(
                        {
                            "Scenario": label,
                            "Total Premium": scenario_data.get("total_premium", 0),
                            "Total Collateral": scenario_data.get("total_collateral", 0),
                            "Contracts Selected": len(scenario_data.get("selected", [])),
                        }
                    )

                results_df = pd.DataFrame(results)
                st.dataframe(results_df, use_container_width=True)

                st.caption("📊 Total Premium by Scenario")
                chart_df = results_df.set_index("Scenario")[["Total Premium"]]
                st.bar_chart(chart_df, use_container_width=True)

                st.caption("📊 Total Collateral by Scenario")
                collateral_chart_df = results_df.set_index("Scenario")[["Total Collateral"]]
                st.bar_chart(collateral_chart_df, use_container_width=True)

                # Auto-summary
                try:
                    base_val = results_df.loc[results_df["Scenario"] == "Base", "Total Premium"].iloc[0]
                    min_val = results_df["Total Premium"].min()
                    max_val = results_df["Total Premium"].max()
                    if base_val == 0:
                        summary = "No premium earned in the base case."
                    else:
                        swing_pct = (max_val - min_val) / base_val
                        if swing_pct <= 0.1:
                            summary = "Your results are stable across premium changes."
                        elif swing_pct <= 0.3:
                            summary = "Your results show moderate sensitivity to premium changes."
                        else:
                            summary = "Your results are highly sensitive to premium changes."
                    st.info(f"🧠 Auto-summary: {summary}")
                except Exception:
                    st.info("🧠 Auto-summary: Unable to compute sensitivity summary.")

    except Exception as e:
        st.error(f"❌ Optimization failed: {e}")
