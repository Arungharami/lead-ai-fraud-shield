"""SHAP-based explainability for Lead.AI Fraud Shield."""

import numpy as np
from typing import Optional
from src.utils import encode_input, score_to_label, FEATURE_COLUMNS, generate_prediction_id
from src.predict import load_model

FEATURE_DISPLAY_NAMES = {
    "transaction_amount":    "Transaction Amount",
    "transaction_hour":      "Transaction Hour",
    "payment_method_encoded":"Payment Method",
    "customer_age":          "Customer Age",
    "account_age_days":      "Account Age (days)",
    "previous_orders":       "Previous Orders",
    "merchant_risk_score":   "Merchant Risk Score",
    "device_risk_score":     "Device Risk Score",
    "location_risk_score":   "Location Risk Score",
}

PAYMENT_METHOD_REVERSE = {3: "crypto", 2: "bank_transfer", 1: "paypal", 0: "card"}


def explain_transaction(data: dict) -> dict:
    """
    Predict and explain a single transaction using SHAP TreeExplainer.

    Returns a dict with risk_label, confidence, risk_score, and full explanation.
    """
    import datetime

    try:
        import shap
    except ImportError:
        raise ImportError("Install shap: `pip install shap`")

    model = load_model()
    X = encode_input(data)

    proba = model.predict_proba(X)[0]
    fraud_score = float(proba[2])
    confidence = float(max(proba))
    risk_label = score_to_label(fraud_score)

    # SHAP explanation for the High Risk class (index 2)
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)

    # shap_values shape: [n_classes, n_samples, n_features]
    # Use class 2 (High Risk) values
    if isinstance(shap_values, list):
        sv = shap_values[2][0]
    else:
        sv = shap_values[0]

    feature_impacts = {
        feat: round(float(sv[i]), 4)
        for i, feat in enumerate(FEATURE_COLUMNS)
    }

    # Sort by absolute impact, take top 3
    sorted_features = sorted(
        feature_impacts.items(), key=lambda x: abs(x[1]), reverse=True
    )[:3]

    top_features = []
    for feat, impact in sorted_features:
        raw_val = X[feat].iloc[0]
        # Decode payment method back to string
        if feat == "payment_method_encoded":
            display_val = PAYMENT_METHOD_REVERSE.get(int(raw_val), "card")
        else:
            display_val = raw_val

        top_features.append({
            "feature": FEATURE_DISPLAY_NAMES.get(feat, feat),
            "value": display_val,
            "shap_impact": impact,
            "direction": "increases_risk" if impact > 0 else "decreases_risk",
        })

    summary = _build_summary(risk_label, top_features)

    return {
        "prediction_id": generate_prediction_id(),
        "risk_label": risk_label,
        "risk_score": round(fraud_score, 4),
        "confidence": round(confidence, 4),
        "explanation": {
            "top_features": top_features,
            "all_features": {
                FEATURE_DISPLAY_NAMES.get(k, k): v
                for k, v in feature_impacts.items()
            },
            "summary": summary,
        },
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "disclaimer": (
            "SHAP values are approximations. "
            "This explanation is for decision-support only, not legal advice."
        ),
    }


def _build_summary(risk_label: str, top_features: list) -> str:
    """Generate a plain-English summary from top SHAP features."""
    if not top_features:
        return f"Transaction classified as {risk_label} based on overall feature profile."

    drivers = [
        f"{f['feature']} ({f['value']})"
        for f in top_features
        if f["direction"] == "increases_risk"
    ]

    if not drivers:
        return f"Transaction classified as {risk_label}. No single dominant risk driver identified."

    driver_text = ", ".join(drivers)
    qualifier = {
        "High Risk": "strongly associated with fraudulent activity",
        "Medium Risk": "associated with elevated transaction risk",
        "Low Risk": "present but outweighed by low-risk signals",
    }.get(risk_label, "predictive of the assigned risk class")

    return (
        f"Transaction flagged as {risk_label} primarily due to: {driver_text}. "
        f"These features are {qualifier} in the training distribution."
    )
