"""
Training pipeline for Lead.AI Fraud Shield.
Trains a GradientBoostingClassifier on synthetic fraud data
and saves the artifact to model/model.joblib.

Run: python src/model.py
"""

import os
import json
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.preprocessing import label_binarize

from src.utils import FEATURE_COLUMNS, PAYMENT_METHOD_MAP

RANDOM_STATE = 42
MODEL_DIR = "model"
MODEL_PATH = os.path.join(MODEL_DIR, "model.joblib")
METRICS_PATH = os.path.join(MODEL_DIR, "metrics.json")


def generate_synthetic_data(n: int = 5000) -> pd.DataFrame:
    """Generate synthetic transaction data for training."""
    rng = np.random.default_rng(RANDOM_STATE)

    data = pd.DataFrame({
        "transaction_amount":    rng.exponential(scale=300, size=n).clip(1, 10000),
        "transaction_hour":      rng.integers(0, 24, size=n),
        "payment_method_encoded":rng.choice([0, 1, 2, 3], size=n, p=[0.6, 0.2, 0.1, 0.1]),
        "customer_age":          rng.integers(18, 80, size=n),
        "account_age_days":      rng.exponential(scale=400, size=n).clip(0, 3650).astype(int),
        "previous_orders":       rng.integers(0, 200, size=n),
        "merchant_risk_score":   rng.beta(2, 5, size=n),
        "device_risk_score":     rng.beta(2, 5, size=n),
        "location_risk_score":   rng.beta(2, 5, size=n),
    })

    # Synthetic fraud label logic
    fraud_score = (
        (data["transaction_amount"] > 800).astype(float) * 0.25
        + (data["transaction_hour"] < 5).astype(float) * 0.20
        + (data["payment_method_encoded"] == 3).astype(float) * 0.20
        + (data["account_age_days"] < 30).astype(float) * 0.15
        + data["device_risk_score"] * 0.10
        + data["merchant_risk_score"] * 0.10
    )
    fraud_score = fraud_score + rng.normal(0, 0.05, size=n)
    fraud_score = fraud_score.clip(0, 1)

    # Map to 3-class labels: 0=Low, 1=Medium, 2=High
    data["risk_class"] = pd.cut(
        fraud_score,
        bins=[-0.001, 0.35, 0.65, 1.0],
        labels=[0, 1, 2]
    ).astype(int)

    return data


def load_data_from_hf() -> pd.DataFrame:
    """Attempt to load dataset from Hugging Face; fall back to synthetic."""
    try:
        from datasets import load_dataset
        print("Loading dataset from Hugging Face...")
        ds = load_dataset("arun-gharami/lead-ai-fraud-detection-dataset-v2", split="train")
        df = ds.to_pandas()

        # Map binary risk_label to 3 classes using thresholds
        df["risk_class"] = pd.cut(
            df["customer_risk_score"].fillna(0.5),
            bins=[-0.001, 0.35, 0.65, 1.0],
            labels=[0, 1, 2]
        ).astype(int)

        df["payment_method_encoded"] = 0  # HF dataset uses different schema
        print(f"Loaded {len(df)} rows from Hugging Face.")
        return df

    except Exception as e:
        print(f"HF load failed ({e}). Using synthetic data.")
        return generate_synthetic_data(n=5000)


def train():
    os.makedirs(MODEL_DIR, exist_ok=True)

    df = load_data_from_hf()

    X = df[FEATURE_COLUMNS]
    y = df["risk_class"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    model = GradientBoostingClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        random_state=RANDOM_STATE,
    )
    print("Training model...")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=["Low Risk", "Medium Risk", "High Risk"])

    print(f"\nAccuracy: {accuracy:.4f}")
    print(report)

    metrics = {
        "accuracy": round(accuracy, 4),
        "training_rows": len(X_train),
        "test_rows": len(X_test),
        "model_type": "GradientBoostingClassifier",
        "features": FEATURE_COLUMNS,
        "classes": ["Low Risk", "Medium Risk", "High Risk"],
        "note": "Trained on synthetic/benchmark data. Not validated on real-world transactions.",
    }

    joblib.dump(model, MODEL_PATH)
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"\nModel saved to {MODEL_PATH}")
    print(f"Metrics saved to {METRICS_PATH}")
    return model


if __name__ == "__main__":
    train()
