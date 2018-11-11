import json

from flask_cors import CORS
from flask import Flask, request
import gateway as gateway

app = Flask(__name__)

CORS(app)


@app.route('/pay/')
def hello_world():
    return 'Hello World!'


@app.route('/pay/client_token/', methods=['GET'])
def new_checkout():
    # app.logger.info('new_checkout(%s)' % customer_id)
    return str(gateway.generate_client_token())


@app.route('/pay/purchase/', methods=['POST'])
def create_subscription():
    data = json.loads(request.data)
    app.logger.info('create_checkout(%s)', data)
    result = gateway.subscription(data)
    app.logger.info('create_checkout() return: %s' % result)

    try:
        return result.subscription.id
    except:
        return str(result), 500


if __name__ == '__main__':
    app.run()
