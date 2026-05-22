"""
Lead.AI Fraud Shield — FastAPI Server

Endpoints:
  GET  /              — API info
  GET  /health        — Health check
  POST /predict       — Score one transaction
  POST /explain       — Score + SHAP explanation
  POST /batch-predict — Score up to 100 transactions
  GET  /model-info    — Model metadata

Run: uvicorn api.main:app --reload
Docs: http://localhost:8000/docs
"""

import os
import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator

from src.predict import predict_transaction, batch_predict, load_model
from src.explain import explain_transaction

# ── App ──────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Lead.AI Fraud Shield API",
    description=(
        "Explainable fraud risk scoring for transactions. "
        "Returns Low/Medium/High risk label with SHAP-based explanation. "
        "Built by Lead.AI Labs — https://www.lead-ai.us"
    ),
    version="1.0.0",
    contact={
        "name": "Arun Kumar Gharami — Lead.AI Labs",
        "url": "https://www.lead-ai.us",
    },
    license_info={"name": "Apache 2.0"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Schemas ───────────────────────────────────────────────────────────────────

class TransactionInput(BaseModel):
    transaction_amount:   float = Field(..., ge=0, le=1_000_000, example=1200.0)
    transaction_hour:     int   = Field(..., ge=0, le=23, example=1)
    payment_method:       str   = Field(..., example="crypto")
    customer_age:         int   = Field(..., ge=18, le=120, example=22)
    account_age_days:     int   = Field(..., ge=0, le=36500, example=8)
    previous_orders:      int   = Field(..., ge=0, le=100_000, example=0)
    merchant_risk_score:  float = Field(..., ge=0.0, le=1.0, example=0.82)
    device_risk_score:    float = Field(..., ge=0.0, le=1.0, example=0.91)
    location_risk_score:  float = Field(..., ge=0.0, le=1.0, example=0.88)

    @validator("payment_method")
    def validate_payment_method(cls, v):
        allowed = {"crypto", "card", "bank_transfer", "paypal"}
        if v.lower() not in allowed:
            raise ValueError(f"payment_method must be one of {allowed}")
        return v.lower()


class BatchInput(BaseModel):
    transactions: list[TransactionInput] = Field(..., max_items=100)


DISCLAIMER = (
    "This prediction is for decision-support only. "
    "Trained on synthetic data. Human review is required for consequential actions. "
    "See LIMITATIONS.md for full details."
)

# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/", tags=["Info"])
def root():
    return {
        "name": "Lead.AI Fraud Shield API",
        "version": "1.0.0",
        "description": "Explainable fraud risk scoring for transactions",
        "docs": "/docs",
        "health": "/health",
        "author": "Arun Kumar Gharami — Lead.AI Labs",
        "website": "https://www.lead-ai.us",
        "huggingface": "https://huggingface.co/arun-gharami/lead-ai-fraud-shield",
        "github": "https://github.com/Arungharami/lead-ai-fraud-shield",
    }


@app.get("/health", tags=["Info"])
def health():
    try:
        load_model()
        model_loaded = True
    except FileNotFoundError:
        model_loaded = False

    return {
        "status": "healthy" if model_loaded else "unhealthy",
        "model_loaded": model_loaded,
        "model_version": "1.0.0",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    }


@app.get("/model-info", tags=["Info"])
def model_info():
    import json
    metrics_path = os.environ.get("METRICS_PATH", "model/metrics.json")
    metrics = {}
    if os.path.exists(metrics_path):
        with open(metrics_path) as f:
            metrics = json.load(f)

    return {
        "model_name": "Lead.AI Fraud Shield",
        "model_version": "1.0.0",
        "model_type": metrics.get("model_type", "GradientBoostingClassifier"),
        "framework": "scikit-learn",
        "training_data": "lead-ai-fraud-detection-dataset-v2 (synthetic, 100K rows)",
        "features": metrics.get("features", []),
        "output_classes": ["Low Risk", "Medium Risk", "High Risk"],
        "benchmark_accuracy": metrics.get("accuracy"),
        "benchmark_note": "Synthetic holdout only — not real-world accuracy",
        "huggingface": "https://huggingface.co/arun-gharami/lead-ai-fraud-shield",
        "author": "Arun Kumar Gharami — Lead.AI Labs",
        "website": "https://www.lead-ai.us",
        "disclaimer": DISCLAIMER,
    }


@app.post("/predict", tags=["Scoring"])
def predict(txn: TransactionInput):
    try:
        result = predict_transaction(txn.dict())
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/explain", tags=["Scoring"])
def explain(txn: TransactionInput):
    try:
        result = explain_transaction(txn.dict())
        return result
    except ImportError:
        # Fall back to predict-only if shap not installed
        result = predict_transaction(txn.dict())
        result["explanation"] = {
            "summary": "Install shap for full explanation: pip install shap",
            "top_features": [],
        }
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Explanation failed: {str(e)}")


@app.post("/batch-predict", tags=["Scoring"])
def batch(body: BatchInput):
    try:
        transactions = [t.dict() for t in body.transactions]
        results = batch_predict(transactions)
        import uuid
        return {
            "batch_id": f"batch_{datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:6]}",
            "count": len(results),
            "results": results,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "disclaimer": DISCLAIMER,
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch prediction failed: {str(e)}")
