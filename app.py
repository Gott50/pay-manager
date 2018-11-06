from flask_cors import CORS
from flask import Flask
import src.gateway as gateway

app = Flask(__name__)

CORS(app)


@app.route('/pay/')
def hello_world():
    return 'Hello World!'


@app.route('/pay/client_token/', methods=['GET'])
def new_checkout():
    # app.logger.info('new_checkout(%s)' % customer_id)
    return str(gateway.generate_client_token())


@app.route('/pay/purchase/<nonce>', methods=['GET'])
def create_subscription(nonce):
    app.logger.info('create_checkout(%s)' % nonce)
    result = gateway.subscription(nonce)
    app.logger.info('create_checkout() return: %s' % result)

    return str(result)

if __name__ == '__main__':
    app.run()
