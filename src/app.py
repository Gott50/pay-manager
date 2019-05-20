import json

from flask_cors import CORS
from flask import Flask, request
from stripe.error import InvalidRequestError

import gateway as gateway

app = Flask(__name__)

CORS(app)

cache = {}

@app.route('/pay/purchase/', methods=['POST'])
def create_subscription():
    data = json.loads(request.data)
    app.logger.warning('create_subscription(%s)', data)

    if data.get('email') in cache:
        app.logger.warning('cached result: ', cache[data.get('email')])
        return cache[data.get('email')]

    try:
        result = gateway.subscription(data, app.logger.warning)
    except InvalidRequestError:
        app.logger.warning('create_checkout() return: No such coupon, 406 Not Acceptable')
        return "No such coupon", 406  # Not Acceptable

    app.logger.warning('create_checkout() return: %s' % result)

    try:
        result_id = result.id
        cache[data.get('email')] = result_id
        return result_id
    except:
        return str(result), 500


if __name__ == '__main__':
    app.run("0.0.0.0", port=7000)
