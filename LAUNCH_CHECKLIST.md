# Launch Checklist — Lead.AI Fraud Shield

**Use this checklist before every public launch, dataset update, or product announcement.**

---

## GitHub Repository

- [ ] `README.md` is complete and up to date
- [ ] `PRODUCT_BRIEF.md`, `BUSINESS_CASE.md`, `PRICING.md` are current
- [ ] `MODEL_CARD.md` matches the deployed model version
- [ ] `API_SPEC.md` matches the actual API endpoints
- [ ] `SECURITY_AND_COMPLIANCE.md` reviewed and accurate
- [ ] `LIMITATIONS.md` is honest and complete
- [ ] `.gitignore` excludes: `.env`, `*.joblib`, `*.csv` (data), `*.key`, `credentials.*`
- [ ] No API keys, tokens, passwords, or secrets committed to the repo
- [ ] `requirements.txt` is up to date and pinned to working versions
- [ ] `model/model.joblib` is excluded from git (download from HF or generate locally)
- [ ] `data/sample_data.csv` contains only synthetic sample rows (≤ 20 rows)
- [ ] All CI/CD checks pass (if configured)
- [ ] GitHub repo description and topics are set (fraud-detection, xai, explainable-ai, etc.)

---

## Hugging Face

- [ ] `lead-ai-fraud-shield` model card updated with current version
- [ ] `lead-ai-fraud-detection-model` model card updated
- [ ] `lead-ai-customer-predictor` model card updated
- [ ] `lead-ai-review-sentinel` model card updated
- [ ] `lead-ai-fraud-detection-dataset` dataset card updated
- [ ] `lead-ai-fraud-detection-dataset-v2` dataset card updated
- [ ] `fraud-detection-xai-demo` Space is running (not sleeping)
- [ ] Profile README is current at `huggingface.co/arun-gharami`
- [ ] All 4 Collections are populated with correct assets
- [ ] YAML frontmatter is valid on all model and dataset cards
- [ ] Tags include: `fraud-detection`, `explainable-ai`, `xai`, `shap`, `lead-ai-labs`

---

## Kaggle

- [ ] Dataset published at kaggle.com/datasets/arungharami
- [ ] Dataset title matches: "Lead.AI Fraud Detection Dataset — 100K Synthetic Benchmark"
- [ ] Dataset description matches `KAGGLE_README.md`
- [ ] Dataset tags include: fraud-detection, tabular, synthetic, XAI, classification
- [ ] Demo notebook published and linked from dataset page
- [ ] Notebook is clean: no errors, all cells run top-to-bottom
- [ ] Links to HF, GitHub, and lead-ai.us are in the notebook

---

## Lead.AI Website (lead-ai.us)

- [ ] Fraud Shield product section is live
- [ ] "Try Demo" button links to HF Space
- [ ] "View Dataset" button links to HF / Kaggle
- [ ] "Deploy for Your Business" links to contact page
- [ ] Contact form is working (test submission)
- [ ] Pricing section matches `PRICING.md`
- [ ] Mobile responsive (test on phone)
- [ ] Page loads under 3 seconds
- [ ] No broken links

---

## Demo

- [ ] HF Space is running and not sleeping
- [ ] Demo produces correct output for the "Try This Scenario" example
- [ ] Demo loads in under 10 seconds
- [ ] Share the demo URL with at least one colleague to verify it works externally

---

## Outreach

- [ ] LinkedIn post drafted and ready to publish
- [ ] LinkedIn post includes: demo link, dataset link, GitHub link, CTA
- [ ] Email pitch template ready (for cold outreach to potential clients)
- [ ] Google Scholar profile updated if new publication/preprint added
- [ ] Hugging Face organization page (Lead.AI Labs) updated with new assets

---

## Optional (Revenue-Enabling)

- [ ] Gumroad product page for Starter ($299) tier
- [ ] Calendly link for consultation bookings on lead-ai.us
- [ ] Stripe or Gumroad payment link for professional tier
- [ ] LinkedIn "Open to consulting" status enabled

---

## LinkedIn Post Template

```
🚀 Launching Lead.AI Fraud Shield — open-source explainable fraud detection for small businesses and FinTech teams.

Every prediction comes with a risk label AND a SHAP explanation — so your team knows not just what to block, but why.

✅ 3-tier risk scoring (Low / Medium / High)
✅ SHAP feature attribution per prediction
✅ FastAPI REST server
✅ 100K synthetic training dataset (Kaggle + Hugging Face)
✅ Free to use, modify, and deploy

👉 Try the live demo: [HF Space URL]
📊 Download the dataset: [Kaggle URL]
💻 Clone the repo: [GitHub URL]
🌐 Commission a custom build: lead-ai.us

Built with scikit-learn · SHAP · Gradio · FastAPI

#FraudDetection #ExplainableAI #XAI #MachineLearning #FinTech #OpenSource #LeadAI #TrustworthyAI
```

---

*Lead.AI Labs — Trustworthy AI Systems for Practical Business Intelligence*
