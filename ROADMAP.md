# Product Roadmap — Lead.AI Fraud Shield

---

## Current Version: v1.0.0

**Status: Open-source benchmark and demonstration system**

### What's Live
- [x] 9-feature tabular classification model (GradientBoostingClassifier)
- [x] 3-tier risk label output (Low / Medium / High)
- [x] SHAP-style feature attribution per prediction
- [x] FastAPI REST server with `/predict`, `/explain`, `/batch-predict`, `/health`
- [x] Gradio interactive demo
- [x] 100K synthetic training dataset (HF + Kaggle)
- [x] Professional model card, dataset card, and documentation
- [x] Apache 2.0 open-source license

---

## v1.1.0 — Model & Feature Improvements

**Target: Q3 2025**

- [ ] Expand from 9 to 21 input features (full dataset schema)
- [ ] Add XGBoost and LightGBM model variants for benchmarking
- [ ] Add probability calibration (Platt scaling / isotonic regression)
- [ ] Improve SHAP explanation with counterfactual: *"If X were Y, the risk would be Low"*
- [ ] Add `risk_score` threshold slider in Gradio demo
- [ ] Add confusion matrix and ROC-AUC to model evaluation output

---

## v1.2.0 — API & Integration Improvements

**Target: Q4 2025**

- [ ] API key authentication (`X-API-Key` header)
- [ ] Rate limiting middleware (per-key, per-IP)
- [ ] Request / response audit logging (structured JSON logs)
- [ ] Docker image published to Docker Hub
- [ ] One-click Railway / Render deployment button
- [ ] Postman collection for the full API
- [ ] Webhook support: POST results to your endpoint on prediction

---

## v2.0.0 — Production-Ready Platform

**Target: Q1 2026**

- [ ] **Fraud Shield Dashboard** — Streamlit or React dashboard
  - Live fraud rate metrics
  - Risk distribution over time
  - SHAP summary plots
  - Manual review queue with approve/reject
- [ ] **Retraining pipeline** — automated weekly model refresh from labeled outcomes
- [ ] **Drift detection** — alert when prediction distribution shifts significantly
- [ ] **Multi-model support** — run fraud-shield + customer-predictor + review-sentinel together
- [ ] **Batch CSV scoring** — upload a CSV, get a scored CSV back
- [ ] **Human-in-the-loop queue** — Medium-risk transactions routed to review interface

---

## v2.1.0 — Enterprise & Compliance

**Target: Q2 2026**

- [ ] **GDPR-aligned logging** — configurable data retention and right-to-erasure support
- [ ] **Adverse action report generator** — generate compliant explanation reports per prediction
- [ ] **Role-based access control** — admin / analyst / read-only roles
- [ ] **White-label mode** — remove Lead.AI branding for OEM/embedded use
- [ ] **On-premise deployment package** — for organizations that cannot use cloud APIs

---

## Research Roadmap

| Item | Description | Timeline |
|------|-------------|----------|
| Graph neural network fraud detection | Model fraud rings and linked accounts | 2025 |
| Real-time streaming fraud scoring | Kafka/Flink integration for sub-50ms scoring | 2025 |
| LLM-enhanced explanations | Use an LLM to generate richer, context-aware explanations | 2025 |
| Fairness audit framework | Automated disparate impact testing across demographic proxies | 2025 |
| Published research paper | Explainable fraud detection for SMBs — XAI survey + benchmark | 2026 |

---

## Feedback & Feature Requests

Have a feature request or use case not covered here?

- **GitHub Issues:** [github.com/Arungharami/lead-ai-fraud-shield/issues](https://github.com/Arungharami/lead-ai-fraud-shield/issues)
- **LinkedIn:** [linkedin.com/in/arunkgharami](https://www.linkedin.com/in/arunkgharami)
- **Website:** [lead-ai.us](https://www.lead-ai.us)

---

*Lead.AI Labs — Trustworthy AI Systems for Practical Business Intelligence*
