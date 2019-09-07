import json
import os

from flask_cors import CORS
from flask import Flask, request, jsonify
from stripe.error import InvalidRequestError

import gateway as gateway

app = Flask(__name__)

CORS(app)

cache_subscription = {}
cache_customer = {}


@app.route('/pay/purchase/', methods=['POST'])
def create_subscription():
    data = json.loads(request.data)
    app.logger.warning('create_subscription(%s)', data)
    email = data.get('email')
    token = data.get('token')

    if os.environ.get('STRIPE_SECRET_KEY') == 'TEST':
        return token

    if email in cache_subscription:
        app.logger.warning('cached result: ', cache_subscription[email])
        return cache_subscription[email]

    try:
        if email in cache_customer:
            customer = cache_customer[email]
        else:
            customer = gateway.get_customer(email=email, source=token, print=app.logger.warning)
            cache_customer[email] = customer

        result = gateway.subscription(customer, data.get('discount_code'), app.logger.warning)
    except InvalidRequestError:
        app.logger.warning('create_checkout() return: No such coupon, 406 Not Acceptable')
        return "No such coupon", 406  # Not Acceptable

    app.logger.warning('create_checkout() return: %s' % result)

    try:
        result_id = result.id
        cache_subscription[email] = result_id
        return result_id
    except Exception as exc:
        app.logger.error("POST /pay/purchase/: " % exc)
        return str(result), 500

@app.route('/pay/customer/update', methods=['POST'])
def update_customer():
    try:
        data = json.loads(request.data)
        app.logger.warning('update_customer(%s)', data)
        email = data.get('email')
        token = data.get('token')

        result = gateway.modify_costomer(email=email, source=token, print=app.logger.warning)
        return result.id
    except Exception as exc:
        app.logger.error("POST /pay/customer/update: " % exc)
        return str(exc), 500  # 500 Internal Server Error


@app.route('/pay/price/discount/<discount_code>', methods=['GET'])
def get_discount(discount_code):
    try:
        app.logger.warning('get_discount(%s)', discount_code)
        return jsonify(gateway.get_coupon(discount_code))
    except Exception as exc:
        app.logger.error("GET /pay/price/discount/%s: " % (discount_code, exc))
        return str(exc), 500  # 500 Internal Server Error


if __name__ == '__main__':
    app.run("0.0.0.0", port=7000)
