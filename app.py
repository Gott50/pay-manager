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


if __name__ == '__main__':
    app.run()
