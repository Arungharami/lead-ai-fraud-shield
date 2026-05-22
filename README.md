# 🛡️ Lead.AI Fraud Shield

### Explainable Fraud Detection & Risk Scoring API for Small Businesses, FinTech Teams, E-commerce, and Payment Platforms

[![Live Demo](https://img.shields.io/badge/🖥️%20Live%20Demo-Try%20Now-blue?style=for-the-badge)](https://huggingface.co/spaces/arun-gharami/fraud-detection-xai-demo)
[![Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-Model-orange?style=for-the-badge)](https://huggingface.co/arun-gharami/lead-ai-fraud-shield)
[![Kaggle Dataset](https://img.shields.io/badge/📊%20Kaggle-Dataset-20BEFF?style=for-the-badge)](https://www.kaggle.com/datasets/arungharami)
[![Lead.AI Labs](https://img.shields.io/badge/🚀%20Deploy-lead--ai.us-FF6B35?style=for-the-badge)](https://www.lead-ai.us)
[![License](https://img.shields.io/badge/License-Apache%202.0-green?style=for-the-badge)](LICENSE)

> **Built by [Lead.AI Labs](https://www.lead-ai.us)** — Trustworthy AI Systems for Practical Business Intelligence  
> Author: [Arun Kumar Gharami](https://huggingface.co/arun-gharami) | [Google Scholar](https://scholar.google.com/citations?user=uy4i5soAAAAJ&hl=en) | [LinkedIn](https://www.linkedin.com/in/arunkgharami)

---

## The Problem

Every undetected fraudulent transaction costs your business 3–5× its face value once you
factor in chargebacks, dispute fees, manual review time, and bank penalties.

Most small businesses and FinTech teams either:
- Have **no fraud detection at all** — relying on manual spot-checks
- Use **black-box rule engines** — that flag everything or nothing, with no explanation
- Can't afford **enterprise fraud platforms** — which cost $50K–$500K/year to license and deploy

**Lead.AI Fraud Shield closes this gap.**

---

## The Solution

A production-ready, open-source fraud risk scoring system that gives you:

| What you get | Why it matters |
|-------------|---------------|
| ✅ Risk label: Low / Medium / High | Route transactions to auto-approve, review, or block |
| ✅ Confidence score (0–100%) | Tune your own threshold per business tolerance |
| ✅ SHAP explanation per prediction | Know *why* a transaction was flagged — audit-ready |
| ✅ REST API (FastAPI) | Plug into any payment stack in hours |
| ✅ Gradio demo | Share with stakeholders before committing to deployment |
| ✅ Open datasets (5K + 100K rows) | Train, benchmark, and publish research |

---

## Live Resources

| Resource | Link |
|----------|------|
| 🖥️ Interactive XAI Demo | [fraud-detection-xai-demo](https://huggingface.co/spaces/arun-gharami/fraud-detection-xai-demo) |
| 🤗 Model: Fraud Shield | [arun-gharami/lead-ai-fraud-shield](https://huggingface.co/arun-gharami/lead-ai-fraud-shield) |
| 🤗 Model: Fraud Detection | [arun-gharami/lead-ai-fraud-detection-model](https://huggingface.co/arun-gharami/lead-ai-fraud-detection-model) |
| 📊 Dataset v1 (5K) | [HF Dataset](https://huggingface.co/datasets/arun-gharami/lead-ai-fraud-detection-dataset) |
| 📊 Dataset v2 (100K) | [HF Dataset v2](https://huggingface.co/datasets/arun-gharami/lead-ai-fraud-detection-dataset-v2) |
| 📓 Kaggle Notebook | [Kaggle](https://www.kaggle.com/datasets/arungharami) |
| 🌐 Lead.AI Website | [lead-ai.us](https://www.lead-ai.us) |

---

## Quickstart

```bash
git clone https://github.com/Arungharami/lead-ai-fraud-shield.git
cd lead-ai-fraud-shield
pip install -r requirements.txt
```

### Run the Gradio Demo Locally

```bash
python src/app.py
# Open http://localhost:7860
```

### Run the FastAPI Server

```bash
uvicorn api.main:app --reload
# Open http://localhost:8000/docs
```

### Score a Single Transaction

```python
from src.predict import predict_transaction

result = predict_transaction({
    "transaction_amount": 1200.0,
    "transaction_hour": 1,
    "payment_method": "crypto",
    "customer_age": 22,
    "account_age_days": 8,
    "previous_orders": 0,
    "merchant_risk_score": 0.82,
    "device_risk_score": 0.91,
    "location_risk_score": 0.88
})

print(result)
# {
#   "risk_label": "High Risk",
#   "confidence": "94.00%",
#   "explanation": "Top risk drivers: device_risk_score, account_age_days, payment_method"
# }
```

---

## API Example

### POST /predict

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_amount": 1200.0,
    "transaction_hour": 1,
    "payment_method": "crypto",
    "customer_age": 22,
    "account_age_days": 8,
    "previous_orders": 0,
    "merchant_risk_score": 0.82,
    "device_risk_score": 0.91,
    "location_risk_score": 0.88
  }'
```

**Response:**
```json
{
  "risk_label": "High Risk",
  "confidence": 0.94,
  "risk_score": 0.94,
  "prediction_id": "pred_20240115_001",
  "timestamp": "2024-01-15T01:23:45Z"
}
```

### POST /explain

```bash
curl -X POST http://localhost:8000/explain \
  -H "Content-Type: application/json" \
  -d '{ "transaction_amount": 1200.0, "transaction_hour": 1, ... }'
```

**Response:**
```json
{
  "risk_label": "High Risk",
  "confidence": 0.94,
  "explanation": {
    "top_features": [
      {"feature": "device_risk_score", "value": 0.91, "impact": "+0.38"},
      {"feature": "account_age_days",  "value": 8,    "impact": "+0.29"},
      {"feature": "payment_method",    "value": "crypto", "impact": "+0.18"}
    ],
    "summary": "Transaction flagged primarily due to high device risk score, very new account, and use of crypto payment — a combination strongly associated with fraud in training data."
  }
}
```

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Client / Business                  │
│    (E-commerce checkout, payment processor, CRM)    │
└──────────────────────┬──────────────────────────────┘
                       │ POST /predict or /explain
┌──────────────────────▼──────────────────────────────┐
│              Lead.AI Fraud Shield API                │
│              FastAPI · /predict /explain             │
│              /batch-predict · /health                │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│              ML Pipeline (src/)                      │
│   Preprocessing → Feature Encoding → GBM Model      │
│   → Risk Label + Confidence + SHAP Attribution       │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│              Model Artifact                          │
│   model/model.joblib · model/metrics.json            │
│   Trained on: lead-ai-fraud-detection-dataset-v2     │
│   (100K synthetic transactions, 21 features)         │
└─────────────────────────────────────────────────────┘
```

---

## Business Use Cases

| Industry | How They Use It |
|----------|----------------|
| **E-commerce** | Score every order at checkout — flag high-risk before fulfillment |
| **FinTech / Lending** | Screen loan applications and disbursements for fraud indicators |
| **Payment Processors** | Pre-authorization risk check — route to manual review above threshold |
| **Subscription Businesses** | Detect trial abuse, account takeover, and synthetic identity fraud |
| **Banks / Credit Unions** | First-pass automated triage before analyst review |
| **Retail** | Flag card-not-present and cross-border orders |

---

## Deployment Options

| Option | Description | Time |
|--------|-------------|------|
| **Hugging Face Spaces** | Deploy Gradio demo — zero infra | Minutes |
| **Local FastAPI** | Run on your own server — full control | Hours |
| **Docker** | Containerized deployment — portable | 1 day |
| **Cloud (AWS / GCP / Azure)** | Scalable production deployment | 1–3 days |
| **Custom integration** | Lead.AI builds it for you — retrained on your data | [Contact us](https://www.lead-ai.us) |

---

## Repository Structure

```
lead-ai-fraud-shield/
├── README.md                    ← You are here
├── PRODUCT_BRIEF.md             ← One-page business summary
├── BUSINESS_CASE.md             ← ROI analysis and use cases
├── MODEL_CARD.md                ← Technical model documentation
├── DATASET_CARD.md              ← Dataset documentation
├── KAGGLE_README.md             ← Kaggle dataset page
├── HUGGINGFACE_README.md        ← Hugging Face model card
├── API_SPEC.md                  ← Full API documentation
├── DEPLOYMENT.md                ← Deployment guide
├── PRICING.md                   ← Service pricing
├── SECURITY_AND_COMPLIANCE.md   ← Security and compliance notes
├── LIMITATIONS.md               ← Honest limitations
├── ROADMAP.md                   ← Product roadmap
├── LAUNCH_CHECKLIST.md          ← Launch checklist
├── LICENSE                      ← Apache 2.0
├── requirements.txt
├── src/
│   ├── app.py                   ← Gradio demo
│   ├── model.py                 ← Training pipeline
│   ├── predict.py               ← Prediction logic
│   ├── explain.py               ← SHAP explanations
│   └── utils.py                 ← Preprocessing utilities
├── api/
│   └── main.py                  ← FastAPI server
├── notebooks/
│   └── lead_ai_fraud_shield_kaggle_demo.ipynb
├── data/
│   └── sample_data.csv          ← 20-row synthetic sample
└── website/
    └── lead-ai-us-product-section.html
```

---

## ⚠️ Important Disclaimer

All models in this repository are trained on **synthetic benchmark data**.
They are intended for **educational, research, prototyping, and decision-support** use only.

- Do not use as the sole basis for financial, legal, or fraud enforcement decisions
- No real customer data is used or stored
- No regulatory certification (FFIEC, PCI-DSS, GDPR) has been obtained
- Production deployment requires validation on real data and compliance review

---

## Commission a Custom Build

Want this running on your real transaction data?

**Lead.AI Labs builds production-ready fraud detection systems for:**
- E-commerce businesses processing 1K–1M+ transactions/month
- FinTech startups needing a fraud layer before they can afford enterprise tools
- Internal risk teams who need explainable AI for analyst workflows

**→ [Start a project at lead-ai.us](https://www.lead-ai.us)**  
**→ [Connect on LinkedIn](https://www.linkedin.com/in/arunkgharami)**

---

## Citation

```bibtex
@misc{gharami2024fraudshield,
  author       = {Arun Kumar Gharami},
  title        = {Lead.AI Fraud Shield: Explainable Fraud Detection and Risk Scoring API},
  year         = {2024},
  publisher    = {GitHub},
  howpublished = {\url{https://github.com/Arungharami/lead-ai-fraud-shield}}
}
```

---

*Lead.AI Labs — Trustworthy AI Systems for Practical Business Intelligence*  
[lead-ai.us](https://www.lead-ai.us) · [LinkedIn](https://www.linkedin.com/in/arunkgharami) · [GitHub](https://github.com/Arungharami) · [Hugging Face](https://huggingface.co/arun-gharami)
