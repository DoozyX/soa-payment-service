#!/usr/bin/env python3
import datetime
import logging
import connexion
import pybreaker
import redis
import socket
import requests
import json

import orm
from DBListener import DBListener

BASE_CONSUL_URL = 'http://consul:8500'
SERVICE_ADDRESS = socket.gethostbyname(socket.gethostname())
PORT = 8081
redis = redis.Redis(host='redis')

db_breaker = pybreaker.CircuitBreaker(
    fail_max=3,
    reset_timeout=20,
    state_storage=pybreaker.CircuitRedisStorage(pybreaker.STATE_CLOSED, redis),
    listeners=[DBListener()]
)


@db_breaker
def get_payments_history(limit):
    q = db_session.query(orm.PaymentHistory)
    return [p.dump() for p in q][:limit]


@db_breaker
def get_payment(payment_id):
    payment = db_session.query(orm.PaymentHistory).filter(orm.PaymentHistory.id == payment_id).one_or_none()
    return payment.dump() if payment is not None else ('Not found', 404)


@db_breaker
def make_payment(payment):
    logging.info('Creating payment')
    payment['created'] = datetime.datetime.utcnow()
    payment['successful'] = True
    db_session.add(orm.PaymentHistory(**payment))
    db_session.commit()
    return {'successful': True}, 201


@db_breaker
def get_credit_card(owner_id):
    logging.info("GETTING CREDIT CARD")
    credit_card = db_session.query(orm.CreditCard).filter(orm.CreditCard.user_id == owner_id).one_or_none()
    return credit_card.dump() if credit_card is not None else ('Not found', 404)


@db_breaker
def add_credit_card(credit_card):
    logging.info('Creating payment')
    db_session.add(orm.CreditCard(**credit_card))
    db_session.commit()
    return {'successful': True}, 201


def health_check():
    data = {
        'status': 'healthy'
    }
    return json.dumps(data)


def register():
    url = BASE_CONSUL_URL + '/v1/agent/service/register'
    data = {
        'Name': 'PythonApp',
        'Tags': ['flask'],
        'Address': SERVICE_ADDRESS,
        'Port': 8080,
        'Check': {
            'http': 'http://{address}:{port}/health'.format(address=SERVICE_ADDRESS, port=PORT),
            'interval': '10s'
        }
    }
    logging.info('Service registration parameters: ', data)
    res = requests.put(
        url,
        data=json.dumps(data)
    )
    return res.text


logging.basicConfig(level=logging.INFO)
db_session = orm.init_db('postgresql://postgres:admin@postgresdb:5432/soa-payment-service')
app = connexion.FlaskApp(__name__)
app.add_api('openapi.yaml')

application = app.app


@application.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    try:
        logging.info(register())
    except:
        logging.info('Something wrong happened!')
        pass
    app.run(debug=True, host="0.0.0.0", port=PORT)
