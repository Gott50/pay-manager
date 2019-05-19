import json

from flask_cors import CORS
from flask import Flask, request
from stripe.error import InvalidRequestError

import gateway as gateway

app = Flask(__name__)

CORS(app)

@app.route('/pay/purchase/', methods=['POST'])
def create_subscription():
    data = json.loads(request.data)
    app.logger.warning('create_checkout(%s)', data)

    try:
        result = gateway.subscription(data, app.logger.warning)
    except InvalidRequestError:
        app.logger.warning('create_checkout() return: No such coupon, 406 Not Acceptable')
        return "No such coupon", 406  # Not Acceptable

    app.logger.warning('create_checkout() return: %s' % result)

    try:
        return result.id
    except:
        return str(result), 500


if __name__ == '__main__':
    app.run("0.0.0.0", port=7000)
