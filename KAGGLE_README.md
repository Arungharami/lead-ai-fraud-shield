# Lead.AI Fraud Detection Dataset — Kaggle

**100,000 Synthetic Transactions · 21 Features · Binary + Multi-class Fraud Labels**

> Published by [Arun Kumar Gharami](https://www.kaggle.com/arungharami) · [Lead.AI Labs](https://www.lead-ai.us)

---

## About This Dataset

This dataset provides a clean, ready-to-use synthetic benchmark for financial fraud
detection research and machine learning experimentation. It contains 100,000 transactions
with behavioral, temporal, geographic, and transaction-type features — all synthetically
generated for safe, unrestricted use.

> ⚠️ **Synthetic data.** No real customer data, no real financial transactions, no PII.
> This dataset is completely safe to use, modify, publish, and share.

---

## What You Can Do With It

| Task | Description |
|------|-------------|
| Binary classification | Predict `risk_label` (0 = normal, 1 = fraud) |
| Multi-class risk scoring | Build a Low / Medium / High risk classifier |
| XAI / SHAP research | Identify which features drive fraud predictions |
| Imbalanced learning | Practice SMOTE, class weighting, threshold tuning |
| Feature engineering | Build velocity features, risk aggregations, time windows |
| Benchmarking | Compare XGBoost, LightGBM, Random Forest, TabNet |

---

## Features

| Feature | Type | Description |
|---------|------|-------------|
| `transaction_id` | string | Unique ID |
| `customer_id` | string | Customer ID |
| `transaction_amount` | float | Transaction value (USD) |
| `transaction_hour` | int | Hour of day (0–23) |
| `transaction_day_of_week` | int | 0=Monday … 6=Sunday |
| `is_weekend` | int | 1 = weekend |
| `account_age_days` | int | Days since account creation |
| `previous_chargebacks` | int | Prior chargeback count |
| `merchant_category` | string | Category of merchant |
| `transaction_country` | string | Country code |
| `geo_location_region` | string | Geographic region |
| `device_type` | string | mobile / desktop / tablet / wearable |
| `transaction_type` | string | online / pos / atm / card_present |
| `is_international` | int | 1 = international |
| `is_high_risk_merchant_category` | int | 1 = high-risk merchant |
| `customer_total_transactions_30d` | int | 30-day transaction count |
| `customer_risk_score` | float | Customer risk (0.0–1.0) |
| `avg_transaction_amount_30d_customer` | float | 30-day average amount |
| `transaction_velocity_1h` | int | Transactions in last hour |
| `transaction_velocity_24h` | int | Transactions in last 24 hours |
| `risk_label` | int | **Target** — 0=normal, 1=fraud |

---

## Load the Data

```python
import pandas as pd

df = pd.read_csv("/kaggle/input/lead-ai-fraud-detection/train.csv")
print(df.shape)
print(df["risk_label"].value_counts())
```

---

## Suggested Notebook Ideas

1. **Baseline Fraud Classifier** — Logistic regression to random forest in 30 minutes
2. **XGBoost + SHAP** — Train a GBM and explain every prediction
3. **Imbalanced Learning** — Compare SMOTE, ADASYN, and class weighting
4. **Feature Engineering** — Build velocity ratios, risk composites, time-of-day bins
5. **Threshold Tuning** — Optimize precision/recall trade-off for a real business scenario
6. **Deep Learning on Tabular Data** — Try TabNet or FT-Transformer
7. **Fraud EDA** — Visualize fraud rates by hour, country, merchant category, and device

---

## Related Resources

| Resource | Link |
|----------|------|
| 🤗 Hugging Face Model | [lead-ai-fraud-shield](https://huggingface.co/arun-gharami/lead-ai-fraud-shield) |
| 🖥️ Live XAI Demo | [fraud-detection-xai-demo](https://huggingface.co/spaces/arun-gharami/fraud-detection-xai-demo) |
| 💻 GitHub | [lead-ai-fraud-shield](https://github.com/Arungharami/lead-ai-fraud-shield) |
| 🌐 Lead.AI Website | [lead-ai.us](https://www.lead-ai.us) |

---

## Citation

```bibtex
@misc{gharami2024fraudkaggle,
  author  = {Arun Kumar Gharami},
  title   = {Lead.AI Fraud Detection Dataset: 100K Synthetic Benchmark},
  year    = {2024},
  url     = {https://www.kaggle.com/datasets/arungharami/lead-ai-fraud-detection}
}
```

---

*Lead.AI Labs — Trustworthy AI Systems for Practical Business Intelligence*
