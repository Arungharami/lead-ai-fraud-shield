.PHONY: install demo api train test

install:
	pip install -r requirements.txt

demo:
	PYTHONPATH=. python3 src/app.py

api:
	PYTHONPATH=. uvicorn api.main:app --reload

train:
	PYTHONPATH=. python3 src/model.py

test:
	PYTHONPATH=. python3 -c "\
from src.predict import predict_transaction; \
r = predict_transaction({'transaction_amount':1200,'transaction_hour':1,'payment_method':'crypto','customer_age':22,'account_age_days':8,'previous_orders':0,'merchant_risk_score':0.82,'device_risk_score':0.91,'location_risk_score':0.88}); \
print('risk_label:', r['risk_label']); \
print('confidence:', r['confidence']); \
print('PASS' if r['risk_label'] in ['Low Risk','Medium Risk','High Risk'] else 'FAIL')"
