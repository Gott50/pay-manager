import json

from flask_cors import CORS
from flask import Flask, request
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

    if data.get('email') in cache_subscription:
        app.logger.warning('cached result: ', cache_subscription[data.get('email')])
        return cache_subscription[data.get('email')]

    try:
        if data.get('email') in cache_customer:
            customer = cache_customer[data.get('email')]
        else:
            customer = gateway.get_customer(data, app.logger.warning)
            cache_customer[data.get('email')] = customer

        result = gateway.subscription(data, customer, app.logger.warning)
    except InvalidRequestError:
        app.logger.warning('create_checkout() return: No such coupon, 406 Not Acceptable')
        return "No such coupon", 406  # Not Acceptable

    app.logger.warning('create_checkout() return: %s' % result)

    try:
        result_id = result.id
        cache_subscription[data.get('email')] = result_id
        return result_id
    except:
        return str(result), 500


if __name__ == '__main__':
    app.run("0.0.0.0", port=7000)
