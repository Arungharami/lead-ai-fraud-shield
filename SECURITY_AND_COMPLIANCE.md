# Security & Compliance — Lead.AI Fraud Shield

---

## Data Security

### What This System Does NOT Store

- ❌ Real credit card numbers, CVVs, or PANs
- ❌ Real customer names, email addresses, phone numbers, or SSNs
- ❌ Real bank account numbers or routing numbers
- ❌ Any PII from real users in the base open-source version

### What the Training Data Contains

All training data is **fully synthetic** — algorithmically generated to simulate
transaction patterns. No real financial data was used to train any model in this repository.

### Handling Real Data in Production

If you retrain this model on your real transaction data:

1. **Store credentials in environment variables** — never hard-code tokens, API keys,
   database passwords, or secrets in source code or committed files
2. **Use `.gitignore`** — ensure `.env`, `*.key`, `credentials.json`, and data files
   are excluded from version control (see `.gitignore` in this repo)
3. **Encrypt data at rest** — use encrypted storage for any real transaction data
4. **Use TLS in transit** — all API calls should be over HTTPS in production
5. **Implement access controls** — restrict API access to authorized services only
6. **Anonymize before training** — remove or hash direct identifiers before using
   real data for model training

---

## Secret Management

```bash
# NEVER do this:
HF_TOKEN = "hf_abc123..."   # hard-coded in source code
STRIPE_KEY = "sk_live_..."  # committed to git

# DO this instead:
import os
HF_TOKEN = os.environ.get("HF_TOKEN")
STRIPE_KEY = os.environ.get("STRIPE_SECRET_KEY")
```

**Recommended secret managers:**
- Local: `.env` file + `python-dotenv` (never commit `.env`)
- AWS: AWS Secrets Manager / Parameter Store
- GCP: Secret Manager
- Azure: Key Vault
- Vercel / Railway / Render: Platform environment variables

---

## Human-in-the-Loop (HITL) Review

**This model is a decision-support tool, not an autonomous enforcement system.**

Recommended review policy:

| Risk Label | Confidence | Recommended Action |
|-----------|-----------|-------------------|
| Low Risk | Any | Auto-approve |
| Medium Risk | < 70% | Human review required |
| Medium Risk | ≥ 70% | Human review recommended |
| High Risk | Any | Block pending human review |

**Never automate account termination, legal action, or fraud enforcement** based
solely on model output without human review and documented justification.

---

## Audit Logging

For production deployments, log every prediction with:

```json
{
  "prediction_id": "pred_20240115_001",
  "timestamp": "2024-01-15T01:23:45Z",
  "input_hash": "sha256_of_input_features",
  "risk_label": "High Risk",
  "confidence": 0.94,
  "action_taken": "flagged_for_review",
  "reviewed_by": null,
  "final_decision": null,
  "model_version": "1.0.0"
}
```

Audit logs enable:
- Regulatory review of automated decisions
- Bias monitoring and fairness audits
- Model performance tracking over time
- Dispute documentation

---

## Explainability Reports

The `/explain` endpoint generates a per-prediction explanation that can be:
- Attached to chargeback dispute filings
- Stored in your case management system
- Shared with compliance officers
- Reviewed by risk analysts

---

## Compliance Disclaimer

> **Lead.AI Fraud Shield has not been reviewed or certified by any financial regulatory body**,
> including but not limited to: FFIEC, PCI-DSS, GDPR, CCPA, CFPB, FCA, or FINRA.
>
> Users are solely responsible for ensuring their deployment complies with all applicable
> laws, regulations, and industry standards in their jurisdiction.
>
> This system is a **decision-support tool**. It must not be used as the sole basis for
> any legally consequential action affecting individuals, including fraud enforcement,
> account suspension, credit denial, or legal proceedings.

---

## Responsible Disclosure

If you discover a security vulnerability in this project, please report it privately:

- Email: [LinkedIn message to Arun Kumar Gharami](https://www.linkedin.com/in/arunkgharami)
- Do not open a public GitHub issue for security vulnerabilities

---

*Lead.AI Labs — Trustworthy AI Systems for Practical Business Intelligence*
