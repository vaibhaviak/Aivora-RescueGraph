import os
import json
from datetime import date
import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv

from rescuegraph import (
    Household, Shock, simulate, detect_first_domino,
    compare_interventions, explain_with_gemini, save_scenario
)

load_dotenv()
st.set_page_config(page_title="Aivora RescueGraph", page_icon="🛟", layout="wide")

st.markdown("""
<style>
.block-container {max-width: 1180px; padding-top: 1.5rem;}
.hero {padding: 1.4rem 1.5rem; border-radius: 18px; background: linear-gradient(120deg,#101d37,#153b54); color:white;}
.hero h1 {color:white; margin-bottom:.25rem;}
.hero p {color:#d8e9f5; font-size:1.03rem;}
.small-muted {color:#68778a; font-size:.88rem;}
</style>
<div class="hero">
<h1>🛟 AIVORA RESCUEGRAPH</h1>
<p>Rehearse financial shocks. Find the first domino. Compare recovery options.</p>
</div>
""", unsafe_allow_html=True)
st.caption("Prototype • Synthetic scenarios only • Not financial advice")

with st.sidebar:
    st.header("Household profile")
    monthly_income = st.number_input("Monthly take-home income (₹)", min_value=0, max_value=10000000, value=60000, step=5000)
    starting_savings = st.number_input("Liquid savings today (₹)", min_value=0, max_value=100000000, value=90000, step=5000)
    essential_expenses = st.number_input("Monthly essential expenses (₹)", min_value=0, max_value=10000000, value=30000, step=1000)
    debt_payment = st.number_input("Monthly debt payments (₹)", min_value=0, max_value=10000000, value=12000, step=1000)
    discretionary = st.number_input("Monthly discretionary expenses (₹)", min_value=0, max_value=10000000, value=5000, step=500)
    st.divider()
    st.header("Stress scenario")
    salary_delay = st.slider("Salary delay (months)", min_value=0, max_value=3, value=1)
    shock_amount = st.number_input("Unexpected one-time expense (₹)", min_value=0, max_value=10000000, value=40000, step=5000)
    shock_month = st.selectbox("Unexpected expense occurs in month", [1, 2, 3, 4, 5, 6], index=0)
    simulation_months = st.slider("Simulation horizon (months)", min_value=3, max_value=12, value=6)
    st.caption("Use fictional data. Do not enter bank credentials or sensitive personal information.")

household = Household(
    monthly_income=float(monthly_income),
    starting_savings=float(starting_savings),
    essential_expenses=float(essential_expenses),
    debt_payment=float(debt_payment),
    discretionary_expenses=float(discretionary),
    salary_delay_months=int(salary_delay),
    horizon_months=int(simulation_months),
)
shock = Shock(amount=float(shock_amount), month=int(shock_month), label="Unexpected expense")

st.subheader("Financial rehearsal")
col1, col2, col3 = st.columns(3)
base = simulate(household, shocks=[])
stress = simulate(household, shocks=[shock])
domino = detect_first_domino(stress)

col1.metric("Starting liquid savings", f"₹{starting_savings:,.0f}")
col2.metric("Baseline minimum balance", f"₹{base['minimum_balance']:,.0f}", help="Lowest projected end-of-month cash balance")
col3.metric("Stress-case minimum", f"₹{stress['minimum_balance']:,.0f}", delta=f"₹{stress['minimum_balance']-base['minimum_balance']:,.0f}", delta_color="normal")

chart_df = pd.DataFrame(stress["months"])
fig = px.line(chart_df, x="month", y="ending_balance", markers=True,
              title="Projected liquid balance under selected stress scenario",
              labels={"month":"Month","ending_balance":"Ending balance (₹)"})
fig.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Zero-cash threshold")
st.plotly_chart(fig, use_container_width=True)

left, right = st.columns([1, 1])
with left:
    st.subheader("First Domino Detector")
    if domino:
        st.error(f"Potential first cash shortfall: Month {domino['month']}")
        st.write(domino["explanation"])
        st.write(f"Projected balance: ₹{domino['balance']:,.0f}")
    else:
        st.success("No negative end-of-month balance detected in this scenario.")
        st.write("A positive balance does not guarantee every bill can be paid on its due date.")
with right:
    st.subheader("Cascade analysis")
    st.write("The deterministic engine checks when projected cash becomes negative and tracks the impact of the selected shock.")
    st.write(f"Stress-case ending balance after {simulation_months} months: **₹{stress['ending_balance']:,.0f}**")
    st.write(f"Stress-case lowest balance: **₹{stress['minimum_balance']:,.0f}**")

st.subheader("Counterfactual intervention lab")
st.write("Compare transparent what-if options. These are illustrative scenarios, not recommendations to skip payments or assume a lender will approve a change.")
expense_reduction = st.slider("Possible discretionary reduction per month (₹)", 0, int(discretionary), min(0, int(discretionary)), step=500 if discretionary >= 500 else 1)
extra_buffer = st.slider("Hypothetical one-time support / reimbursement (₹)", 0, 50000, 0, step=5000)
if st.button("Compare interventions", type="primary"):
    options = compare_interventions(
        household, [shock],
        discretionary_reduction=float(expense_reduction),
        one_time_support=float(extra_buffer)
    )
    st.dataframe(pd.DataFrame(options), use_container_width=True, hide_index=True)
    st.session_state["last_options"] = options

st.subheader("Gemini recovery analyst")
st.write("Gemini explains the computed scenario. It does not calculate the balances and must not invent financial facts.")
if st.button("Generate AI explanation"):
    with st.spinner("Analysing computed scenario with Gemini..."):
        result = explain_with_gemini(household, stress, domino)
        st.session_state["ai_result"] = result
if "ai_result" in st.session_state:
    st.markdown(st.session_state["ai_result"])

with st.expander("Show transparent assumptions and monthly data"):
    st.json({
        "income": monthly_income,
        "starting_savings": starting_savings,
        "essential_expenses": essential_expenses,
        "debt_payment": debt_payment,
        "discretionary_expenses": discretionary,
        "salary_delay_months": salary_delay,
        "shock": {"label": shock.label, "amount": shock.amount, "month": shock.month},
        "calculation_method": "Opening cash + received income - essential expenses - debt payments - discretionary expenses - shock expenses",
        "important_limit": "Monthly simulation; does not model exact intra-month payment dates, interest, fees, taxes, or actual financial product terms."
    })
    st.dataframe(pd.DataFrame(stress["months"]), use_container_width=True, hide_index=True)

if st.button("Save this synthetic scenario to Firestore (optional)"):
    try:
        result = save_scenario({
            "created_at": date.today().isoformat(),
            "profile": {
                "monthly_income": monthly_income,
                "starting_savings": starting_savings,
                "essential_expenses": essential_expenses,
                "debt_payment": debt_payment,
                "discretionary_expenses": discretionary,
                "salary_delay_months": salary_delay
            },
            "shock": {"amount": shock.amount, "month": shock.month},
            "stress_result": stress
        })
        st.success(f"Scenario saved. Record ID: {result}")
    except Exception as e:
        st.warning(f"Firestore is not configured or unavailable: {e}")

st.divider()
st.caption("Aivora RescueGraph is an educational prototype using user-defined synthetic scenarios. It does not access bank accounts, predict actual crises, provide regulated financial advice, or execute payments.")
