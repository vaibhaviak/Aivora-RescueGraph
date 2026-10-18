# Aivora RescueGraph

**A financial crisis rehearsal prototype** that models user-defined synthetic cash-flow shocks, detects the first negative month-end balance, compares possible interventions, and can use Gemini to explain the deterministic results when configured.

> Educational prototype only. It does not connect to banks, predict actual crises, execute payments, or provide regulated financial advice.

## Features
- Editable household assumptions and shock scenario
- Deterministic monthly cash-flow engine
- First Domino Detector for the first projected negative month-end balance
- Counterfactual comparison of spending reduction and hypothetical support
- Optional Gemini explanation grounded in calculated outputs (requires a valid API key)
- Optional Firestore persistence (requires cloud credentials and proper IAM)
- Streamlit interface and Plotly timeline

## Architecture
- Gemini API via `google-genai`: explanation and recovery framing
- Python: cash-flow calculations and scenario comparison
- Streamlit + Plotly: UI and timeline
- Firestore: optional persistence
- Cloud Run: deployment

The prototype uses a deterministic Python engine for calculations rather than asking an LLM to do arithmetic.

## Run locally
Python 3.11+ recommended.

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your own Gemini API key to .env; never commit .env
streamlit run app.py
```

The simulator works without Gemini; the AI explanation requires a valid `GEMINI_API_KEY` and an accessible model. Check current model access in Google AI Studio.

## Tests
```bash
pip install pytest
pytest -q
```

## Deploy to Cloud Run
1. Create a Google Cloud project and enable billing if required.
2. Enable Cloud Run, Cloud Build and Secret Manager APIs.
3. Create a secret named `GEMINI_API_KEY` and grant the Cloud Run service identity permission to access it.
4. Deploy this directory using Cloud Run source deployment or the included Dockerfile.
5. Configure `GEMINI_MODEL` to a model available to your account.
6. For Firestore, enable Firestore in Native mode and grant the runtime service account only the necessary database permissions.
7. Test the public URL in a private browser window and check Cloud Run logs.

Example after configuring the secret and service account:
```bash
gcloud run deploy aivora-rescuegraph \\
  --source . \\
  --region asia-south1 \\
  --allow-unauthenticated \\
  --set-env-vars GEMINI_MODEL=gemini-2.5-flash \\
  --set-secrets GEMINI_API_KEY=GEMINI_API_KEY:latest
```

**Security:** The demo is unauthenticated and intended only for synthetic data. Before using personal financial data, add authentication, authorization, strict Firestore rules, retention/deletion controls, input validation and privacy disclosures. Do not collect bank credentials.

## Firebase / Firestore
The code includes optional Firestore persistence via Google Cloud Application Default Credentials. Do not claim Firebase Authentication or Firebase Hosting is implemented until those services are actually configured and verified. The Firestore write path should not be exposed to untrusted users without appropriate access controls.

## Known limitations
- Month-end rather than daily cash-flow modelling
- No interest, fees, tax, overdraft or actual product terms
- No bank integrations or event prediction
- Inputs are user-defined; outputs are conditional, not forecasts
- Firestore write path needs IAM configuration and should be disabled for unauthenticated public use until access controls are added

## Demo narrative
1. Start with fictional household inputs.
2. Apply a salary delay and unexpected expense.
3. Show the cash balance timeline and first negative month, if any.
4. Compare the baseline with interventions.
5. Demonstrate Gemini and Firestore only if configured and verified.
6. Show the source repository, test results and Cloud Run deployment.

## License
No license is currently included. Choose one after deciding how you want to permit reuse.
