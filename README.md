soa-payment-service

http://localhost:8000/app/payments

curl -i -X POST --url localhost:8001/services --data 'name=app' --data 'url=http://app:8081'
curl -i -X POST --url localhost:8001/services/app/routes --data 'paths[]=/app'