# Deployment Guide — Lead.AI Fraud Shield

---

## Option 1: Local Development (Fastest Start)

```bash
git clone https://github.com/Arungharami/lead-ai-fraud-shield.git
cd lead-ai-fraud-shield
pip install -r requirements.txt

# Train the model (or download from HF)
python src/model.py

# Run Gradio demo
python src/app.py
# → http://localhost:7860

# Run FastAPI server
uvicorn api.main:app --reload
# → http://localhost:8000/docs
```

---

## Option 2: Hugging Face Spaces (Zero Infra Demo)

1. Fork this repo or create a new HF Space
2. Set SDK to `gradio` in the Space metadata
3. Upload `src/app.py`, `model/model.joblib`, `requirements.txt`
4. The Space runs automatically — share the URL

```bash
# Upload to an existing Space
hf upload arun-gharami/fraud-detection-xai-demo src/app.py app.py --repo-type space
```

---

## Option 3: Docker (Portable Production)

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python src/model.py   # train model on startup if no artifact exists

EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t lead-ai-fraud-shield .
docker run -p 8000:8000 lead-ai-fraud-shield
```

---

## Option 4: AWS EC2 / Lambda

### EC2 (always-on)
```bash
# On EC2 instance (Ubuntu)
sudo apt update && sudo apt install python3-pip -y
git clone https://github.com/Arungharami/lead-ai-fraud-shield.git
cd lead-ai-fraud-shield && pip install -r requirements.txt
python src/model.py

# Run with gunicorn for production
pip install gunicorn
gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Lambda (serverless, low traffic)
- Use `Mangum` adapter to wrap FastAPI for Lambda
- Package model artifact in Lambda layer or load from S3
- Configure API Gateway for HTTP endpoint

---

## Option 5: Google Cloud Run

```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/YOUR_PROJECT/fraud-shield

# Deploy
gcloud run deploy fraud-shield \
  --image gcr.io/YOUR_PROJECT/fraud-shield \
  --platform managed \
  --allow-unauthenticated \
  --port 8000
```

---

## Option 6: Railway / Render / Fly.io (1-click PaaS)

These platforms deploy directly from GitHub with zero infra configuration.

**Railway:**
1. Connect GitHub repo
2. Set start command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
3. Deploy

**Render:**
1. New Web Service → Connect repo
2. Build command: `pip install -r requirements.txt && python src/model.py`
3. Start command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MODEL_PATH` | Path to model artifact | `model/model.joblib` |
| `FRAUD_SHIELD_API_KEY` | API key for auth (production) | None (open in dev) |
| `LOG_LEVEL` | Logging level | `INFO` |
| `MAX_BATCH_SIZE` | Max transactions per batch request | `100` |
| `PORT` | Server port | `8000` |

Never hard-code secrets. Use `.env` files locally and platform secret managers in production.

---

## Production Checklist

- [ ] Model retrained on your real transaction data
- [ ] API key authentication enabled
- [ ] Rate limiting configured
- [ ] HTTPS / TLS termination enabled
- [ ] Audit logging active (log every prediction + outcome)
- [ ] Health check monitored (uptime tool)
- [ ] Model drift monitoring scheduled (weekly/monthly)
- [ ] Backup model artifact stored in object storage (S3/GCS)
- [ ] Human review queue configured for Medium-risk predictions
- [ ] PII handling policy documented

---

## Custom Deployment by Lead.AI Labs

Want Lead.AI to deploy and manage this for your business?

**→ [lead-ai.us](https://www.lead-ai.us)**  
**→ [LinkedIn](https://www.linkedin.com/in/arunkgharami)**

Includes: retraining on your data, API deployment, monitoring setup, and 30-day support.

---

*Lead.AI Labs — Trustworthy AI Systems for Practical Business Intelligence*
