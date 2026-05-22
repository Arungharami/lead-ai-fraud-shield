"""Preprocessing and feature encoding utilities for Lead.AI Fraud Shield."""

import pandas as pd
import numpy as np
from typing import Union

PAYMENT_METHOD_MAP = {
    "crypto": 3,
    "bank_transfer": 2,
    "paypal": 1,
    "card": 0,
}

FEATURE_COLUMNS = [
    "transaction_amount",
    "transaction_hour",
    "payment_method_encoded",
    "customer_age",
    "account_age_days",
    "previous_orders",
    "merchant_risk_score",
    "device_risk_score",
    "location_risk_score",
]

RISK_THRESHOLDS = {
    "low":    (0.0, 0.35),
    "medium": (0.35, 0.65),
    "high":   (0.65, 1.0),
}


def encode_input(data: dict) -> pd.DataFrame:
    """Convert a raw input dict to a model-ready DataFrame."""
    payment_method = str(data.get("payment_method", "card")).lower()
    encoded = PAYMENT_METHOD_MAP.get(payment_method, 0)

    row = {
        "transaction_amount":   float(data["transaction_amount"]),
        "transaction_hour":     int(data["transaction_hour"]),
        "payment_method_encoded": encoded,
        "customer_age":         int(data["customer_age"]),
        "account_age_days":     int(data["account_age_days"]),
        "previous_orders":      int(data["previous_orders"]),
        "merchant_risk_score":  float(data["merchant_risk_score"]),
        "device_risk_score":    float(data["device_risk_score"]),
        "location_risk_score":  float(data["location_risk_score"]),
    }
    return pd.DataFrame([row])[FEATURE_COLUMNS]


def score_to_label(score: float) -> str:
    """Map a fraud probability score to a risk label."""
    if score < RISK_THRESHOLDS["medium"][0]:
        return "Low Risk"
    elif score < RISK_THRESHOLDS["high"][0]:
        return "Medium Risk"
    return "High Risk"


def format_confidence(score: float) -> str:
    return f"{score * 100:.2f}%"


def generate_prediction_id() -> str:
    import uuid, datetime
    ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    uid = str(uuid.uuid4())[:6]
    return f"pred_{ts}_{uid}"
