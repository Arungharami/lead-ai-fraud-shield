"""Prediction logic for Lead.AI Fraud Shield."""

import os
import joblib
import numpy as np
from typing import Optional
from src.utils import encode_input, score_to_label, format_confidence, generate_prediction_id

MODEL_PATH = os.environ.get("MODEL_PATH", "model/model.joblib")
_model = None


def load_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            print(f"Model not found at {MODEL_PATH}. Auto-training on synthetic data...")
            from src.model import train
            train()
        _model = joblib.load(MODEL_PATH)
    return _model


def predict_transaction(data: dict) -> dict:
    """
    Score a single transaction.

    Args:
        data: dict with keys: transaction_amount, transaction_hour, payment_method,
              customer_age, account_age_days, previous_orders,
              merchant_risk_score, device_risk_score, location_risk_score

    Returns:
        dict with risk_label, confidence, risk_score, prediction_id
    """
    import datetime

    model = load_model()
    X = encode_input(data)

    proba = model.predict_proba(X)[0]
    fraud_score = float(proba[2])           # probability of High Risk class
    confidence = float(max(proba))
    risk_label = score_to_label(fraud_score)

    return {
        "prediction_id": generate_prediction_id(),
        "risk_label": risk_label,
        "risk_score": round(fraud_score, 4),
        "confidence": round(confidence, 4),
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "model_version": "1.0.0",
        "disclaimer": (
            "This prediction is for decision-support only. "
            "Human review is required for consequential actions."
        ),
    }


def batch_predict(transactions: list[dict]) -> list[dict]:
    """Score multiple transactions. Max 100 per call."""
    if len(transactions) > 100:
        raise ValueError("Maximum 100 transactions per batch request.")
    return [predict_transaction(t) for t in transactions]
