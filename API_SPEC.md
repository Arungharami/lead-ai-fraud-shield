# API Specification — Lead.AI Fraud Shield

**FastAPI · REST · JSON**

Base URL (local): `http://localhost:8000`  
Base URL (production): Configured per deployment — see [DEPLOYMENT.md](DEPLOYMENT.md)

---

## Authentication

The base open-source version runs without authentication for local/demo use.
For production deployment, add an API key header:

```
X-API-Key: your-api-key-here
```

Configure via environment variable: `FRAUD_SHIELD_API_KEY`

---

## Endpoints

---

### GET /

Welcome endpoint — confirms the API is running.

**Request:** None

**Response:**
```json
{
  "name": "Lead.AI Fraud Shield API",
  "version": "1.0.0",
  "description": "Explainable fraud risk scoring for transactions",
  "docs": "/docs",
  "health": "/health",
  "author": "Arun Kumar Gharami — Lead.AI Labs",
  "website": "https://www.lead-ai.us"
}
```

---

### GET /health

Health check — confirms model is loaded and API is ready.

**Request:** None

**Response (healthy):**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Response (unhealthy):**
```json
{
  "status": "unhealthy",
  "model_loaded": false,
  "error": "Model file not found at model/model.joblib"
}
```

---

### POST /predict

Score a single transaction. Returns risk label, confidence score, and prediction ID.

**Request Body:**
```json
{
  "transaction_amount": 1200.0,
  "transaction_hour": 1,
  "payment_method": "crypto",
  "customer_age": 22,
  "account_age_days": 8,
  "previous_orders": 0,
  "merchant_risk_score": 0.82,
  "device_risk_score": 0.91,
  "location_risk_score": 0.88
}
```

**Field Constraints:**

| Field | Type | Required | Range |
|-------|------|----------|-------|
| `transaction_amount` | float | ✅ | 0.0 – 1,000,000 |
| `transaction_hour` | int | ✅ | 0 – 23 |
| `payment_method` | string | ✅ | `crypto` / `card` / `bank_transfer` / `paypal` |
| `customer_age` | int | ✅ | 18 – 120 |
| `account_age_days` | int | ✅ | 0 – 36500 |
| `previous_orders` | int | ✅ | 0 – 100000 |
| `merchant_risk_score` | float | ✅ | 0.0 – 1.0 |
| `device_risk_score` | float | ✅ | 0.0 – 1.0 |
| `location_risk_score` | float | ✅ | 0.0 – 1.0 |

**Response (200):**
```json
{
  "prediction_id": "pred_20240115_a3f7c2",
  "risk_label": "High Risk",
  "risk_score": 0.94,
  "confidence": 0.94,
  "timestamp": "2024-01-15T01:23:45Z",
  "model_version": "1.0.0",
  "disclaimer": "This prediction is for decision-support only. Human review is required for consequential actions."
}
```

**Error (422 — Validation Error):**
```json
{
  "detail": [
    {
      "loc": ["body", "transaction_hour"],
      "msg": "ensure this value is less than or equal to 23",
      "type": "value_error.number.not_le"
    }
  ]
}
```

---

### POST /explain

Score a transaction AND return SHAP-based feature attribution.

**Request Body:** Same as `/predict`

**Response (200):**
```json
{
  "prediction_id": "pred_20240115_a3f7c2",
  "risk_label": "High Risk",
  "risk_score": 0.94,
  "confidence": 0.94,
  "explanation": {
    "top_features": [
      {
        "feature": "device_risk_score",
        "value": 0.91,
        "shap_impact": 0.38,
        "direction": "increases_risk"
      },
      {
        "feature": "account_age_days",
        "value": 8,
        "shap_impact": 0.29,
        "direction": "increases_risk"
      },
      {
        "feature": "payment_method",
        "value": "crypto",
        "shap_impact": 0.18,
        "direction": "increases_risk"
      }
    ],
    "summary": "Transaction flagged primarily due to high device risk score (0.91), very new account (8 days old), and use of crypto payment method — a combination strongly associated with fraudulent activity in the training distribution.",
    "all_features": {
      "device_risk_score": 0.38,
      "account_age_days": 0.29,
      "payment_method": 0.18,
      "merchant_risk_score": 0.06,
      "transaction_amount": 0.04,
      "location_risk_score": 0.03,
      "transaction_hour": 0.02,
      "previous_orders": -0.05,
      "customer_age": -0.01
    }
  },
  "timestamp": "2024-01-15T01:23:46Z",
  "disclaimer": "SHAP values are approximations. This explanation is for decision-support only."
}
```

---

### POST /batch-predict

Score multiple transactions in one request. Returns a list of predictions.

**Request Body:**
```json
{
  "transactions": [
    {
      "transaction_id": "TXN001",
      "transaction_amount": 1200.0,
      "transaction_hour": 1,
      "payment_method": "crypto",
      "customer_age": 22,
      "account_age_days": 8,
      "previous_orders": 0,
      "merchant_risk_score": 0.82,
      "device_risk_score": 0.91,
      "location_risk_score": 0.88
    },
    {
      "transaction_id": "TXN002",
      "transaction_amount": 45.0,
      "transaction_hour": 14,
      "payment_method": "card",
      "customer_age": 35,
      "account_age_days": 720,
      "previous_orders": 42,
      "merchant_risk_score": 0.12,
      "device_risk_score": 0.08,
      "location_risk_score": 0.05
    }
  ]
}
```

**Limits:** Max 100 transactions per request.

**Response (200):**
```json
{
  "batch_id": "batch_20240115_x9k2m1",
  "count": 2,
  "results": [
    {
      "transaction_id": "TXN001",
      "risk_label": "High Risk",
      "risk_score": 0.94,
      "confidence": 0.94
    },
    {
      "transaction_id": "TXN002",
      "risk_label": "Low Risk",
      "risk_score": 0.07,
      "confidence": 0.93
    }
  ],
  "timestamp": "2024-01-15T01:23:50Z",
  "disclaimer": "Batch predictions are for decision-support only."
}
```

---

### GET /model-info

Returns metadata about the loaded model.

**Response (200):**
```json
{
  "model_name": "Lead.AI Fraud Shield",
  "model_version": "1.0.0",
  "model_type": "GradientBoostingClassifier",
  "framework": "scikit-learn",
  "training_data": "lead-ai-fraud-detection-dataset-v2 (synthetic, 100K rows)",
  "features": [
    "transaction_amount",
    "transaction_hour",
    "payment_method",
    "customer_age",
    "account_age_days",
    "previous_orders",
    "merchant_risk_score",
    "device_risk_score",
    "location_risk_score"
  ],
  "output_classes": ["Low Risk", "Medium Risk", "High Risk"],
  "benchmark_accuracy": 0.803,
  "benchmark_note": "Synthetic holdout only — not real-world accuracy",
  "huggingface": "https://huggingface.co/arun-gharami/lead-ai-fraud-shield",
  "author": "Arun Kumar Gharami — Lead.AI Labs",
  "website": "https://www.lead-ai.us",
  "disclaimer": "Trained on synthetic data. Real-world accuracy not validated."
}
```

---

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 422 | Validation error — check field types and ranges |
| 429 | Rate limit exceeded (production only) |
| 500 | Internal server error — model load failure |
| 503 | Service unavailable — model not loaded |

---

## Running the API Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# View interactive docs
open http://localhost:8000/docs

# View ReDoc documentation
open http://localhost:8000/redoc
```

---

## Rate Limits (Production Recommendation)

| Tier | Requests/minute | Requests/day |
|------|----------------|--------------|
| Demo / Free | 10 | 100 |
| Starter | 60 | 5,000 |
| Professional | 300 | 50,000 |
| Enterprise | Custom | Custom |

---

*Lead.AI Labs — Trustworthy AI Systems for Practical Business Intelligence*  
[lead-ai.us](https://www.lead-ai.us) · [LinkedIn](https://www.linkedin.com/in/arunkgharami)
