#!/usr/bin/env python3
import datetime
import logging

import connexion

import orm


def get_payments_history(limit):
    q = db_session.query(orm.PaymentHistory)
    return [p.dump() for p in q][:limit]


def get_payment(payment_id):
    payment = db_session.query(orm.PaymentHistory).filter(orm.PaymentHistory.id == payment_id).one_or_none()
    return payment.dump() if payment is not None else ('Not found', 404)


def make_payment(payment):
    logging.info('Creating payment')
    payment['created'] = datetime.datetime.utcnow()
    payment['successful'] = True
    db_session.add(orm.PaymentHistory(**payment))
    db_session.commit()
    return {'successful': True}, 201


def get_credit_card(owner_id):
    logging.info("GETTING CREDIT CARD")
    credit_card = db_session.query(orm.CreditCard).filter(orm.CreditCard.user_id == owner_id).one_or_none()
    return credit_card.dump() if credit_card is not None else ('Not found', 404)


def add_credit_card(credit_card):
    logging.info('Creating payment')
    db_session.add(orm.CreditCard(**credit_card))
    db_session.commit()
    return {'successful': True}, 201


logging.basicConfig(level=logging.INFO)
db_session = orm.init_db('postgresql://postgres:admin@postgresdb:5432/soa-payment-service')
app = connexion.FlaskApp(__name__)
app.add_api('openapi.yaml')

application = app.app


@application.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run(port=8081, use_reloader=False, threaded=False)
