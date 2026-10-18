from dataclasses import dataclass
from typing import List, Optional
import os
import json

@dataclass
class Household:
    monthly_income: float
    starting_savings: float
    essential_expenses: float
    debt_payment: float
    discretionary_expenses: float
    salary_delay_months: int = 0
    horizon_months: int = 6

@dataclass
class Shock:
    amount: float
    month: int
    label: str = "Unexpected expense"

def simulate(household: Household, shocks: Optional[List[Shock]] = None,
             discretionary_reduction: float = 0.0,
             one_time_support: float = 0.0):
    shocks = shocks or []
    cash = float(household.starting_savings)
    months = []
    for month in range(1, household.horizon_months + 1):
        opening = cash
        income = household.monthly_income if month > household.salary_delay_months else 0.0
        support = one_time_support if month == 1 else 0.0
        shock_total = sum(s.amount for s in shocks if s.month == month)
        reduction = min(max(discretionary_reduction, 0.0), household.discretionary_expenses)
        outflow = household.essential_expenses + household.debt_payment + max(0.0, household.discretionary_expenses - reduction)
        cash = opening + income + support - outflow - shock_total
        months.append({
            "month": month,
            "opening_balance": round(opening, 2),
            "income_received": round(income, 2),
            "one_time_support": round(support, 2),
            "essential_expenses": round(household.essential_expenses, 2),
            "debt_payment": round(household.debt_payment, 2),
            "discretionary_expenses": round(max(0.0, household.discretionary_expenses - reduction), 2),
            "unexpected_expenses": round(shock_total, 2),
            "ending_balance": round(cash, 2),
            "negative_balance": cash < 0
        })
    balances = [m["ending_balance"] for m in months]
    return {
        "months": months,
        "minimum_balance": round(min(balances) if balances else household.starting_savings, 2),
        "ending_balance": round(cash, 2),
        "first_negative_month": next((m["month"] for m in months if m["ending_balance"] < 0), None)
    }

def detect_first_domino(result):
    for row in result["months"]:
        if row["ending_balance"] < 0:
            shortfall = abs(row["ending_balance"])
            return {
                "month": row["month"],
                "balance": row["ending_balance"],
                "explanation": (
                    f"Under the entered assumptions, projected month {row['month']} "
                    f"ends with a cash shortfall of ₹{shortfall:,.0f}. This is the first "
                    "negative month-end balance in the simulation, not proof that a real "
                    "payment will fail. Exact due dates and available credit are not modelled."
                )
            }
    return None

def compare_interventions(household, shocks, discretionary_reduction=0.0, one_time_support=0.0):
    scenarios = [
        ("Selected stress scenario", simulate(household, shocks)),
        ("Reduce discretionary spending", simulate(household, shocks, discretionary_reduction=discretionary_reduction)),
        ("Add hypothetical one-time support", simulate(household, shocks, one_time_support=one_time_support)),
        ("Combine selected interventions", simulate(household, shocks, discretionary_reduction=discretionary_reduction, one_time_support=one_time_support)),
    ]
    rows = []
    for name, result in scenarios:
        rows.append({
            "scenario": name,
            "minimum_balance_in_horizon": result["minimum_balance"],
            "ending_balance": result["ending_balance"],
            "first_negative_month": result["first_negative_month"] or "None in horizon"
        })
    return rows

def explain_with_gemini(household, result, domino):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return (
            "Gemini is not configured. Add GEMINI_API_KEY as an environment secret to enable "
            "the AI explanation. The cash-flow simulation remains available without Gemini."
        )
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        prompt = f"""
You are the explanation agent for Aivora RescueGraph, an educational financial resilience prototype.
Explain the provided computed results in plain English.
Do not recalculate or alter the numeric results. Do not claim certainty about future events.
Do not advise users to skip debt payments, take loans, or purchase financial products.
Suggest practical, low-risk next steps and explicitly label them as options to investigate.
Explain assumptions and limitations. This is not regulated financial advice.
Household inputs: {json.dumps(household.__dict__)}
Computed simulation: {json.dumps(result)}
First negative month: {json.dumps(domino)}
Return concise Markdown with headings: What the simulation says, Main vulnerability, Options to investigate, Assumptions and limits.
"""
        response = client.models.generate_content(model=model, contents=prompt)
        return response.text or "Gemini returned no text. Please retry."
    except Exception as exc:
        return f"Gemini explanation unavailable: {type(exc).__name__}. The deterministic simulation is still usable."

def save_scenario(payload):
    from google.cloud import firestore
    client = firestore.Client()
    doc = client.collection("rescuegraph_scenarios").document()
    doc.set(payload)
    return doc.id
