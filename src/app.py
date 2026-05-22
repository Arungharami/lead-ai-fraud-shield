"""
Gradio demo for Lead.AI Fraud Shield.
Run: python src/app.py
"""

import gradio as gr
from src.predict import predict_transaction
from src.explain import explain_transaction


DISCLAIMER = (
    "⚠️ **Research & Demo Only.** This model is trained on synthetic data and is intended "
    "for educational and prototyping use only. Do not use for real fraud enforcement decisions. "
    "[Learn more](https://www.lead-ai.us)"
)

CSS = """
.risk-high   { color: #dc2626; font-weight: bold; font-size: 1.2em; }
.risk-medium { color: #d97706; font-weight: bold; font-size: 1.2em; }
.risk-low    { color: #16a34a; font-weight: bold; font-size: 1.2em; }
"""


def run_analysis(
    transaction_amount, transaction_hour, payment_method,
    customer_age, account_age_days, previous_orders,
    merchant_risk_score, device_risk_score, location_risk_score
):
    data = {
        "transaction_amount":  transaction_amount,
        "transaction_hour":    transaction_hour,
        "payment_method":      payment_method,
        "customer_age":        customer_age,
        "account_age_days":    account_age_days,
        "previous_orders":     previous_orders,
        "merchant_risk_score": merchant_risk_score,
        "device_risk_score":   device_risk_score,
        "location_risk_score": location_risk_score,
    }

    try:
        result = explain_transaction(data)
    except ImportError:
        result = predict_transaction(data)
        result["explanation"] = {"summary": "Install shap for full explanation: pip install shap"}

    risk = result["risk_label"]
    confidence_pct = f"{result['confidence'] * 100:.1f}%"
    summary = result.get("explanation", {}).get("summary", "No explanation available.")

    top_feat_text = ""
    for f in result.get("explanation", {}).get("top_features", []):
        arrow = "↑" if f["direction"] == "increases_risk" else "↓"
        top_feat_text += f"  {arrow} {f['feature']}: {f['value']} (impact: {f['shap_impact']:+.3f})\n"

    output = f"""**Risk Label:** {risk}
**Confidence:** {confidence_pct}

**Explanation:**
{summary}

**Top Risk Drivers:**
{top_feat_text if top_feat_text else '  No dominant drivers identified.'}

---
*Prediction ID: {result.get('prediction_id', 'N/A')}*
*{DISCLAIMER}*"""

    return output


with gr.Blocks(title="Lead.AI Fraud Shield — XAI Demo", css=CSS) as demo:
    gr.Markdown("""
# 🛡️ Lead.AI Fraud Shield — Explainable Fraud Detection Demo

Score any transaction for fraud risk and see **exactly why** the model flagged it.

> Built by [Arun Kumar Gharami](https://huggingface.co/arun-gharami) · [Lead.AI Labs](https://www.lead-ai.us)
""")

    with gr.Row():
        with gr.Column():
            gr.Markdown("### Transaction Details")
            txn_amount = gr.Slider(0, 10000, value=500, step=10, label="Transaction Amount ($)")
            txn_hour   = gr.Slider(0, 23, value=14, step=1,  label="Transaction Hour (0–23)")
            pay_method = gr.Dropdown(
                ["card", "bank_transfer", "paypal", "crypto"],
                value="card", label="Payment Method"
            )
            cust_age   = gr.Slider(18, 90, value=35, step=1, label="Customer Age")

        with gr.Column():
            gr.Markdown("### Risk Signals")
            acc_age    = gr.Slider(0, 3650, value=365, step=1, label="Account Age (days)")
            prev_orders= gr.Slider(0, 500, value=20, step=1,  label="Previous Orders")
            merch_risk = gr.Slider(0.0, 1.0, value=0.2, step=0.01, label="Merchant Risk Score")
            dev_risk   = gr.Slider(0.0, 1.0, value=0.1, step=0.01, label="Device Risk Score")
            loc_risk   = gr.Slider(0.0, 1.0, value=0.1, step=0.01, label="Location Risk Score")

    analyze_btn = gr.Button("🔍 Analyze Transaction", variant="primary")
    output_box  = gr.Markdown(label="Risk Assessment")

    analyze_btn.click(
        fn=run_analysis,
        inputs=[txn_amount, txn_hour, pay_method, cust_age,
                acc_age, prev_orders, merch_risk, dev_risk, loc_risk],
        outputs=output_box,
    )

    gr.Markdown("""
---
### Try This High-Risk Scenario
Set: **Amount=$1200 · Hour=1 · Method=crypto · Account Age=8 days · Device Risk=0.91**

→ Expected result: **High Risk ~94% confidence**

---
🚀 **Want this for your business?** → [lead-ai.us](https://www.lead-ai.us)
📊 **Dataset** → [Hugging Face](https://huggingface.co/datasets/arun-gharami/lead-ai-fraud-detection-dataset-v2)
💻 **GitHub** → [lead-ai-fraud-shield](https://github.com/Arungharami/lead-ai-fraud-shield)
""")


if __name__ == "__main__":
    demo.launch(share=False)
