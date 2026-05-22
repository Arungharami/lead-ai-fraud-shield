# Limitations — Lead.AI Fraud Shield

Honest, complete documentation of what this system cannot do.

---

## Data Limitations

| Limitation | Detail |
|-----------|--------|
| **Synthetic training data** | Trained entirely on algorithmically generated transactions. Real-world fraud distributions are substantially more complex and variable. |
| **Fixed feature schema** | The model expects exactly 9 features in a specific format. Real-world transaction data will require feature engineering to match this schema. |
| **English-language context** | Risk signals are calibrated for Western payment patterns (US, UK, CA, AU). Cross-border or non-Western fraud patterns are underrepresented. |
| **Static training distribution** | The model was trained on a single synthetic snapshot. Real fraud patterns change over time; the model will degrade without retraining. |

---

## Model Limitations

| Limitation | Detail |
|-----------|--------|
| **Benchmark accuracy is not real-world accuracy** | 80.30% accuracy on a synthetic holdout does not predict accuracy on your real transactions. |
| **No uncertainty calibration** | Confidence scores are model probabilities, not calibrated probabilities. A 94% confidence does not mean a 94% chance of being correct. |
| **Class imbalance sensitivity** | The model was trained on a synthetic class distribution. Your real fraud rate may be very different, requiring threshold re-tuning. |
| **No temporal modeling** | The model does not model time-series patterns or sequential transaction behavior. It scores each transaction independently. |
| **No network/graph features** | Fraud rings, shared devices, and linked accounts are not modeled. |
| **9 features only** | The full dataset has 21 features. The model uses 9. Additional features could improve performance significantly. |

---

## Explainability Limitations

| Limitation | Detail |
|-----------|--------|
| **SHAP values are approximations** | TreeExplainer SHAP values are exact for tree models, but the natural-language summary is a simplification. |
| **Correlation ≠ causation** | A high SHAP value for `device_risk_score` means it was predictive in the training data — not that it caused the fraud. |
| **Explanation may not match analyst intuition** | The model may flag features that seem irrelevant to a human analyst while missing features that seem obvious. |
| **Not a legal explanation** | SHAP output is not a legally compliant explanation for adverse actions under FCRA, GDPR, or similar regulations without additional legal review. |

---

## Deployment Limitations

| Limitation | Detail |
|-----------|--------|
| **No built-in auth in base version** | The FastAPI server in this repo runs open — you must add authentication for production. |
| **No built-in rate limiting** | Implement rate limiting via your reverse proxy (nginx, Caddy) or API gateway. |
| **No built-in PII filtering** | The API does not detect or redact PII in inputs. Never send real card numbers or SSNs to this endpoint. |
| **Model artifact not included in repo** | Run `python src/model.py` to train and generate `model/model.joblib` before starting the API. |
| **Gradio demo is single-threaded** | The Gradio app is for demonstration only. It is not designed for concurrent production traffic. |

---

## What This System Is NOT

- ❌ Not a certified fraud detection platform (no FFIEC, PCI-DSS, or GDPR certification)
- ❌ Not a replacement for human fraud analysts
- ❌ Not suitable for automated legal or enforcement actions without review
- ❌ Not trained on real bank, payment processor, or financial institution data
- ❌ Not a credit scoring model (prohibited use under FCRA in the US)
- ❌ Not a guarantee against fraud losses

---

## How to Mitigate These Limitations

| Limitation | Mitigation |
|-----------|-----------|
| Synthetic data | Retrain on your real labeled transaction history |
| Fixed schema | Add a feature engineering layer to map your data to the model schema |
| Class imbalance | Tune Low/Medium/High thresholds using your actual chargeback rate |
| No temporal modeling | Add rolling velocity and sequence features during preprocessing |
| No auth | Add `X-API-Key` header validation in `api/main.py` |
| No calibration | Use Platt scaling or isotonic regression to calibrate confidence scores |

**Lead.AI Labs can implement all of these mitigations as part of a paid engagement.**  
**→ [lead-ai.us](https://www.lead-ai.us)**

---

*Lead.AI Labs — Trustworthy AI Systems for Practical Business Intelligence*
