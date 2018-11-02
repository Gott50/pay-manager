import os
from dotenv import load_dotenv
import braintree

load_dotenv()

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        environment=os.environ.get('BT_ENVIRONMENT'),
        merchant_id=os.environ.get('BT_MERCHANT_ID'),
        public_key=os.environ.get('BT_PUBLIC_KEY'),
        private_key=os.environ.get('BT_PRIVATE_KEY')
    )
)


def generate_client_token(customer_id=None):
    return gateway.client_token.generate({
        "customer_id": customer_id
    })
