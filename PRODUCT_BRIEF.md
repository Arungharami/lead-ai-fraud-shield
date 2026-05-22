# Lead.AI Fraud Shield — Product Brief

**One-Page Business Summary**

---

## What It Is

**Lead.AI Fraud Shield** is an explainable fraud risk scoring API that classifies financial
transactions as Low / Medium / High risk and explains *why* — using SHAP-based feature
attribution — so analysts, operators, and compliance teams can act with confidence.

---

## The Problem

| Pain Point | Impact |
|-----------|--------|
| Fraud goes undetected until chargeback | 3–5× cost of original transaction |
| Black-box risk engines have no explanation | Analysts can't investigate or override |
| Enterprise fraud platforms cost $50K–$500K/year | Out of reach for SMBs and early-stage FinTechs |
| Manual review doesn't scale | Ops teams bottleneck at 50–200 reviews/day |

---

## Who It Helps

| Customer | Use Case |
|---------|----------|
| **E-commerce stores** | Flag risky orders before fulfillment |
| **FinTech startups** | Fraud layer before they can afford Kount or Sift |
| **Payment processors** | Pre-auth risk check with explainable output |
| **Subscription SaaS** | Trial abuse and synthetic identity detection |
| **Internal risk teams** | AI-assisted triage for analyst queues |
| **Banks & credit unions** | First-pass automated screening |

---

## Product Benefits

| Feature | Benefit |
|---------|---------|
| 3-tier risk label (Low/Medium/High) | Simple routing: approve / review / block |
| Confidence score per prediction | Tune your threshold to match your risk tolerance |
| SHAP explanation per decision | Audit trail for disputes and compliance |
| FastAPI REST interface | Integrates in hours, not months |
| Open-source core | Inspect, fork, and customize freely |
| Synthetic training data | No data privacy constraints during prototyping |

---

## Deployment Options

| Tier | Description | Best For |
|------|-------------|----------|
| **Open Source** | Self-host, modify, train on your own data | Developers, researchers |
| **Managed Demo** | Hugging Face Spaces — zero infra | Stakeholder demos, POC |
| **Starter Integration** | Lead.AI deploys and configures for your stack | SMBs, startups |
| **Professional** | Custom model + dashboard + API | Growing FinTech teams |
| **Enterprise** | Full production system, retraining, monitoring | Scale deployments |

→ See full pricing at [PRICING.md](PRICING.md)

---

## Technical Snapshot

- **Model:** Gradient Boosting Classifier (scikit-learn)
- **Explainability:** SHAP TreeExplainer
- **API:** FastAPI — `/predict`, `/explain`, `/batch-predict`
- **Interface:** Gradio demo
- **Training data:** 100K synthetic transactions, 21 features
- **Benchmark accuracy:** 80.30% on synthetic holdout
- **Serialization:** joblib

---

## Sales CTA

> "Lead.AI Fraud Shield gives your team an explainable fraud risk score for every
> transaction — in milliseconds, with a plain-English reason — so you stop chargebacks
> before they happen and spend analyst time where it actually matters."

**Ready to deploy for your business?**

- 🌐 [lead-ai.us](https://www.lead-ai.us)
- 💼 [linkedin.com/in/arunkgharami](https://www.linkedin.com/in/arunkgharami)
- 🤗 [Try the Live Demo](https://huggingface.co/spaces/arun-gharami/fraud-detection-xai-demo)

---

*Lead.AI Labs · Trustworthy AI Systems for Practical Business Intelligence*
