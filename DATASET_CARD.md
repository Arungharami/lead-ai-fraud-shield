# Dataset Card — Lead.AI Fraud Detection Dataset v2

---

## Dataset Summary

A synthetic tabular benchmark dataset of 100,000 financial transactions labeled as
fraud or normal, with 21 behavioral, temporal, geographic, and transaction-type features.
Designed for training and evaluating explainable fraud detection models.

> ⚠️ **Synthetic Data.** This dataset is entirely algorithmically generated.
> It contains no real customer data, no real financial transactions, and no PII.
> It is safe to use, share, and publish without data governance restrictions.

---

## Where to Find It

| Platform | Link |
|----------|------|
| Hugging Face (v1 — 5K rows) | [arun-gharami/lead-ai-fraud-detection-dataset](https://huggingface.co/datasets/arun-gharami/lead-ai-fraud-detection-dataset) |
| Hugging Face (v2 — 100K rows) | [arun-gharami/lead-ai-fraud-detection-dataset-v2](https://huggingface.co/datasets/arun-gharami/lead-ai-fraud-detection-dataset-v2) |
| Kaggle | [kaggle.com/datasets/arungharami](https://www.kaggle.com/datasets/arungharami) |
| This repo | `data/sample_data.csv` (20-row sample) |

---

## Dataset Details

| Property | v1 | v2 |
|----------|----|----|
| Rows | 5,000 | 100,000 |
| Features | 14 | 21 |
| Format | Parquet | Parquet |
| License | Apache 2.0 | Apache 2.0 |
| Target | `risk_label` (0/1) | `risk_label` (0/1) |

---

## Column Descriptions

| Column | Type | Description |
|--------|------|-------------|
| `transaction_id` | string | Unique transaction identifier |
| `customer_id` | string | Unique customer identifier |
| `transaction_amount` | float | Transaction value in USD |
| `transaction_hour` | int | Hour of day (0–23) |
| `transaction_day_of_week` | int | Day of week (0=Mon … 6=Sun) |
| `is_weekend` | int | 1 = weekend transaction |
| `account_age_days` | int | Days since account creation |
| `previous_chargebacks` | int | Historical chargeback count |
| `merchant_category` | string | gambling / travel / fuel / electronics / etc. |
| `transaction_country` | string | Country code (US, CA, UK, AU, etc.) |
| `geo_location_region` | string | North America / Europe / Asia-Pacific / etc. |
| `device_type` | string | mobile / desktop / tablet / wearable |
| `transaction_type` | string | online / pos / atm_withdrawal / card_present_moto |
| `is_international` | int | 1 = international transaction |
| `is_high_risk_merchant_category` | int | 1 = high-risk merchant |
| `customer_total_transactions_30d` | int | Customer's 30-day transaction count |
| `customer_risk_score` | float | Aggregated customer risk (0.0–1.0) |
| `avg_transaction_amount_30d_customer` | float | Customer's 30-day average amount |
| `transaction_velocity_1h` | int | Transactions in last 1 hour |
| `transaction_velocity_24h` | int | Transactions in last 24 hours |
| `risk_label` | int | **Target** — 0 = normal, 1 = fraud |

---

## How to Load

### Python / pandas
```python
import pandas as pd
df = pd.read_parquet(
    "hf://datasets/arun-gharami/lead-ai-fraud-detection-dataset-v2/data/train-00000-of-00001.parquet"
)
print(df.shape)            # (100000, 21)
print(df["risk_label"].value_counts())
```

### Hugging Face datasets library
```python
from datasets import load_dataset
ds = load_dataset("arun-gharami/lead-ai-fraud-detection-dataset-v2")
df = ds["train"].to_pandas()
```

### Kaggle (in a notebook)
```python
import pandas as pd
df = pd.read_csv("/kaggle/input/lead-ai-fraud-detection/train.csv")
```

---

## Data Quality Notes

- All values are synthetically generated with controlled distributions
- Class imbalance mirrors realistic fraud rates (approximately 10–20% fraud)
- Categorical features use a fixed vocabulary — no free-text or open-ended values
- No missing values in the base dataset
- No duplicate transaction IDs

---

## Limitations

- Synthetic distributions may not reflect your specific business fraud patterns
- Geographic and device features encode synthetic assumptions about risk
- Class balance may differ from your real transaction mix
- Temporal patterns are simulated, not from real seasonality data

---

## Bias and Fairness Note

Features such as `transaction_country`, `geo_location_region`, and `merchant_category`
may encode assumptions that do not reflect real fraud distributions. Users should audit
for proxy discrimination before deploying a model trained on this data in any context
affecting real individuals.

---

## Suggested ML Tasks

- Binary fraud classification (`risk_label` 0/1)
- Multi-class risk scoring (Low / Medium / High)
- XAI / SHAP feature attribution research
- Imbalanced classification (SMOTE, class weighting, threshold tuning)
- Gradient boosting benchmarking (XGBoost, LightGBM, CatBoost)
- Deep learning on tabular data (TabNet, FT-Transformer)

---

## Citation

```bibtex
@misc{gharami2024frauddatasetv2,
  author       = {Arun Kumar Gharami},
  title        = {Lead.AI Fraud Detection Dataset v2: 100K Synthetic Benchmark},
  year         = {2024},
  publisher    = {Hugging Face / Kaggle},
  howpublished = {\url{https://huggingface.co/datasets/arun-gharami/lead-ai-fraud-detection-dataset-v2}}
}
```

---

*Lead.AI Labs — Trustworthy AI Systems for Practical Business Intelligence*
