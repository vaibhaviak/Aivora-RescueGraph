# Pitch deck content — Aivora RescueGraph
**Important:** Use the prescribed challenge template for the final submission. This is supporting content, not a substitute for the official template.

## Slide 1 — Aivora RescueGraph
**Rehearse financial shocks. Find the first domino. Compare recovery options.**
BFSI: Intelligent Risk, Fraud & Financial Experiences

## Slide 2 — The problem
Households can look stable on a monthly budget while timing mismatches and multiple unexpected events create a short-term cash shortfall. Existing summaries may show the balance but not make the chain of dependencies and intervention trade-offs easy to understand.

## Slide 3 — The solution
RescueGraph lets users rehearse compound financial shocks using transparent assumptions, identifies the first projected negative month-end balance, compares hypothetical interventions and can explain the results with Gemini when the API is configured.

## Slide 4 — What is different
- First Domino Detector: highlights the first projected cash shortfall.
- Counterfactual intervention lab: compares explicit scenarios.
- Deterministic calculations with an optional AI explanation layer.
- Clear assumptions and limitations rather than a black-box financial score.

## Slide 5 — How it works
User-defined profile → shock scenario → Python cash-flow engine → first-shortfall detection → intervention comparison → optional Gemini explanation → human-reviewed options.

## Slide 6 — Google technology
Gemini through Google's GenAI SDK for explanations; Python for deterministic calculations; Streamlit and Plotly for the interface; Firestore for optional persistence; Cloud Run for deployment. Firebase Authentication/Hosting must only be listed after implemented and tested.

## Slide 7 — Impact and safety
The prototype aims to make financial stress-testing more understandable and actionable. It uses synthetic data, does not connect to banks, does not execute payments, and does not provide regulated financial advice. Results depend on user-defined assumptions.

## Slide 8 — Evaluation
Test with labelled synthetic scenarios. Measure first-shortfall detection accuracy, calculation correctness, intervention comparison correctness, AI explanation grounding and response latency. Report actual results after running the tests; do not invent metrics.

## Slide 9 — Demo
Show live inputs, a shock scenario, the balance timeline, first domino, intervention comparison, Gemini only if available, and deployment.

## Slide 10 — Roadmap
Add daily cash-flow dates, secure authentication, user-controlled data retention, better evidence handling and optional alerts only after privacy, security and evaluation are addressed.
