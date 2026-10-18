# 3:30 demo script — Aivora RescueGraph

**0:00–0:20 — Hook**
"Most budgets show whether money adds up. RescueGraph asks a different question: when several shocks collide, which obligation becomes unfundable first, and what can we do about it?"

**0:20–0:45 — Introduce the app**
Show the deployed application and state that the demo uses synthetic financial data.

**0:45–1:25 — Configure a scenario**
Show income, savings, essential expenses, debt payment, salary delay and an unexpected expense. Point out the explicit assumptions.

**1:25–2:00 — First Domino Detector**
Show the projected balance chart and first negative month-end balance, if the chosen inputs produce one. Explain that this is a conditional simulation, not a prediction of actual events.

**2:00–2:40 — Counterfactual interventions**
Compare reducing discretionary spending and hypothetical one-time support. Explain how the calculated minimum and ending balances change. Do not imply the support is guaranteed.

**2:40–3:05 — Gemini explanation**
Click Generate AI Explanation. Show how Gemini explains the deterministic results and states limitations. If Gemini authentication is unavailable, state that clearly and skip this step.

**3:05–3:30 — Technical proof**
Show a real test run, Firestore persistence only if configured and verified, and the Cloud Run URL. Finish with: "RescueGraph turns financial stress-testing into an explainable, actionable rehearsal."

## Recording checklist
- Record the deployed app, not only a slide deck.
- Confirm the demo takes 3:00–4:00.
- Use only synthetic data.
- Do not show API keys, secrets, personal data or console credentials.
- Only demonstrate Firebase/Firestore features that work in the deployed version.
