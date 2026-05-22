# Model Card — Lead.AI Fraud Shield

---

## Model Overview

| Property | Value |
|----------|-------|
| **Model name** | Lead.AI Fraud Shield |
| **Task** | Tabular classification — transaction fraud risk scoring |
| **Output** | 3-class: Low Risk / Medium Risk / High Risk |
| **Explainability** | SHAP-style feature attribution per prediction |
| **Framework** | scikit-learn (GradientBoostingClassifier) |
| **Serialization** | joblib |
| **Training data** | Synthetic — lead-ai-fraud-detection-dataset-v2 (100K rows) |
| **License** | Apache 2.0 |
| **Author** | Arun Kumar Gharami — Lead.AI Labs |

---

## Intended Use

### Appropriate Uses
- Transaction risk scoring for e-commerce, FinTech, and payment platforms
- AI-assisted triage for manual fraud review queues
- Decision-support tool for fraud analysts
- Research into explainable fraud detection methods
- Prototyping and proof-of-concept for fraud detection products
- Educational demonstrations of XAI in financial ML contexts

### Not Intended For
- Sole basis for fraud enforcement, account termination, or legal action
- Replacement for human review on high-stakes decisions
- Processing or storing real PII customer financial data in the base version
- Regulatory compliance certification without additional validation
- Credit scoring or lending decisions

---

## Input Features

| Feature | Type | Range / Values | Description |
|---------|------|---------------|-------------|
| `transaction_amount` | float | 0 – 100,000 | Transaction value in USD |
| `transaction_hour` | int | 0 – 23 | Hour of transaction |
| `payment_method` | categorical | crypto / card / bank_transfer / paypal | Payment channel |
| `customer_age` | int | 18 – 90 | Customer age in years |
| `account_age_days` | int | 0 – 3650 | Days since account creation |
| `previous_orders` | int | 0 – 10,000 | Historical order count |
| `merchant_risk_score` | float | 0.0 – 1.0 | Merchant-level risk indicator |
| `device_risk_score` | float | 0.0 – 1.0 | Device fingerprint risk indicator |
| `location_risk_score` | float | 0.0 – 1.0 | Geographic risk indicator |

---

## Output Format

```json
{
  "risk_label": "High Risk",
  "confidence": 0.94,
  "risk_score": 0.94,
  "explanation": {
    "top_features": [
      {"feature": "device_risk_score", "value": 0.91, "impact": "+0.38"},
      {"feature": "account_age_days",  "value": 8,    "impact": "+0.29"},
      {"feature": "payment_method",    "value": "crypto", "impact": "+0.18"}
    ],
    "summary": "Transaction flagged primarily due to high device risk, new account age, and crypto payment method."
  }
}
```

| Output Field | Type | Description |
|-------------|------|-------------|
| `risk_label` | string | `Low Risk` / `Medium Risk` / `High Risk` |
| `confidence` | float | Model probability for the predicted class (0.0–1.0) |
| `risk_score` | float | Fraud probability score (0.0–1.0) |
| `explanation.top_features` | array | SHAP-ranked feature attributions |
| `explanation.summary` | string | Plain-English explanation for analysts |

---

## Training & Evaluation

### Training Data
- **Dataset:** lead-ai-fraud-detection-dataset-v2 (synthetic)
- **Rows:** 100,000 transactions
- **Features used:** 9 of 21 available
- **Split:** 80% train / 20% test (stratified by `risk_label`)
- **Class imbalance handling:** Stratified split; recommend SMOTE or class weighting for production

### Benchmark Metrics (Synthetic Holdout)

| Metric | Value |
|--------|-------|
| Accuracy | 80.30% |
| Training data | Synthetic only |
| Real-world accuracy | Not yet evaluated |

> ⚠️ These metrics are computed on a **synthetic holdout set**. They are not predictive
> of real-world performance. Retrain and evaluate on your own labeled data before production use.

---

## Explainability

This model uses **SHAP (SHapley Additive exPlanations)** TreeExplainer to compute
per-prediction feature attributions. For each prediction, the model surfaces:

1. **Top 3 features** by absolute SHAP value magnitude
2. **Direction of impact** (positive = toward fraud, negative = toward safe)
3. **Plain-English summary** for non-technical users

This enables:
- Analyst-readable decision rationale
- Audit trail generation per transaction
- Bias detection and fairness monitoring
- Model debugging and feature importance tracking

---

## Responsible AI & Ethical Limitations

- **Synthetic training data:** The model has not been validated on real-world transaction data.
  Performance on real data may be substantially different.
- **Proxy bias risk:** Features like `location_risk_score` and `payment_method` may act as
  proxies for demographic attributes. Audit for disparate impact before production deployment.
- **No regulatory certification:** This model has not been reviewed by FFIEC, PCI-DSS, GDPR,
  CFPB, or any other financial regulatory body.
- **False positive cost:** Incorrectly flagging legitimate customers damages trust and
  increases customer service load. Threshold tuning is required per deployment.
- **Concept drift:** Fraud patterns evolve rapidly. A model trained today will degrade
  without periodic retraining on fresh labeled data.
- **Human oversight required:** This model is a decision-support tool. A human must review
  and approve consequential decisions affecting customers.

---

## Production Recommendations

Before deploying in a production financial system:

1. **Retrain on your data** — use your own labeled transaction history
2. **Tune thresholds** — set Low/Medium/High boundaries based on your chargeback tolerance
3. **Evaluate on real holdout** — measure precision, recall, and F1 on held-out real data
4. **Implement HITL review** — route Medium risk to human analysts, not automated action
5. **Add audit logging** — log every prediction, explanation, and action taken
6. **Monitor for drift** — track prediction distribution and retrain every 30–90 days
7. **Run bias audit** — check for disparate impact across demographic groups

---

## Citation

```bibtex
@misc{gharami2024fraudshield,
  author       = {Arun Kumar Gharami},
  title        = {Lead.AI Fraud Shield: Explainable Transaction Fraud Risk Scorer},
  year         = {2024},
  publisher    = {Hugging Face},
  howpublished = {\url{https://huggingface.co/arun-gharami/lead-ai-fraud-shield}}
}
```

---

*Lead.AI Labs — Trustworthy AI Systems for Practical Business Intelligence*
